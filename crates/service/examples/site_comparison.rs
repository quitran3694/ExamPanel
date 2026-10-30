//! Site comparison: a digitised manual plan versus the cold-start optimizer on the same roster.
//!
//! Reads one JSON input (teachers, rule settings, the manual plan as recorded by the group),
//! evaluates the manual plan with the same scorer and validator the app uses, runs the optimizer,
//! and writes a Markdown report plus a JSON score file. Every figure is printed by the program.
//!
//! Teacher identities are codes (GV01…). The input must never contain real names.
//!
//! Usage:
//!   cargo run -p exam-panel-service --example site_comparison -- <input.json> [output_dir]
//!
//! Input shape (see `docs/edu/site3/site3_input.json`):
//!   { "campuses": ["PH1", ...],
//!     "min_campuses": { "VL": 2, "CN": 1 },
//!     "teachers": [{ "code": "GV01", "campus": "PH3", "setter": ["VL"], "reviewer": ["VL", "CN"],
//!                    "unavailable": ["CK1"] }],
//!     "manual_plan": [{ "exam": "GK1", "grade": 10, "subject": "VL", "role": "setter",
//!                       "position": 0, "teacher": "GV01" }] }

use exam_panel_core::domain::{
    Assignment, Campus, CampusId, Competency, Exam, ExamId, Grade, GradeId, GradeScope, Problem,
    Role, RuleKey, RuleSetting, SchoolYear, SchoolYearId, Subject, SubjectId, Teacher,
    TeacherGrade, TeacherId, Unavailability,
};
use exam_panel_core::feasibility::check_feasibility;
use exam_panel_core::optimize::{optimize, Budget, OptimizeOptions};
use exam_panel_core::score::{evaluate, ScoreReport};
use exam_panel_core::validate::{validate_assignments, ValidateOptions};
use serde::Deserialize;
use std::collections::BTreeMap;
use std::fmt::Write as _;
use std::fs;
use std::path::PathBuf;

const BASE_SEED: u64 = 42;
const NUM_RUNS: usize = 8;
const ITERATIONS: u64 = 200_000;
const EXAMS: [(&str, &str); 4] = [
    ("GK1", "Giữa kỳ 1"),
    ("CK1", "Cuối kỳ 1"),
    ("GK2", "Giữa kỳ 2"),
    ("CK2", "Cuối kỳ 2"),
];

#[derive(Deserialize)]
struct InTeacher {
    code: String,
    campus: String,
    setter: Vec<String>,
    reviewer: Vec<String>,
    #[serde(default)]
    unavailable: Vec<String>,
    /// Grades the teacher teaches; defaults to 10, 11 and 12.
    #[serde(default)]
    grades: Vec<i64>,
}

#[derive(Deserialize)]
struct InAssignment {
    exam: String,
    grade: i64,
    subject: String,
    role: String,
    position: usize,
    teacher: String,
}

#[derive(Deserialize)]
struct Input {
    campuses: Vec<String>,
    min_campuses: BTreeMap<String, u8>,
    teachers: Vec<InTeacher>,
    manual_plan: Vec<InAssignment>,
}

fn subject_id(code: &str) -> SubjectId {
    SubjectId(if code == "VL" { 1 } else { 2 })
}

fn build_problem(inp: &Input) -> Problem {
    let campus_id = |code: &str| {
        CampusId(
            inp.campuses
                .iter()
                .position(|c| c == code)
                .expect("unknown campus") as i64
                + 1,
        )
    };
    let exam_id = |code: &str| {
        ExamId(
            EXAMS
                .iter()
                .position(|(c, _)| *c == code)
                .expect("unknown exam") as i64
                + 1,
        )
    };
    let subject = |id: i64, code: &str, name: &str, setters: u8| Subject {
        id: SubjectId(id),
        code: code.to_string(),
        name: name.to_string(),
        color: format!("palette-{id}"),
        sort_order: id as u32,
        setters,
        reviewers: 1,
        min_campuses: *inp.min_campuses.get(code).unwrap_or(&1),
    };
    let teachers: Vec<Teacher> = inp
        .teachers
        .iter()
        .enumerate()
        .map(|(i, t)| Teacher {
            id: TeacherId(i as i64 + 1),
            full_name: format!("Giáo viên {}", t.code),
            campus_id: campus_id(&t.campus),
            load_weight: 1.0,
            active: true,
            note: None,
            code: Some(t.code.clone()),
            display_name: Some(t.code.clone()),
            quota_override: None,
            max_tasks_per_exam_override: None,
        })
        .collect();
    let mut teacher_grades = Vec::new();
    let mut competencies = Vec::new();
    let mut unavailabilities = Vec::new();
    for (i, t) in inp.teachers.iter().enumerate() {
        let tid = TeacherId(i as i64 + 1);
        let taught: Vec<i64> = if t.grades.is_empty() {
            vec![10, 11, 12]
        } else {
            t.grades.clone()
        };
        for g in taught {
            teacher_grades.push(TeacherGrade {
                teacher_id: tid,
                school_year_id: SchoolYearId(1),
                grade_id: GradeId(g - 9),
            });
        }
        for (role, list) in [(Role::Setter, &t.setter), (Role::Reviewer, &t.reviewer)] {
            for s in list {
                // Reviewing a subject the teacher does not set is allowed for any grade.
                let scope = if role == Role::Reviewer && !t.setter.contains(s) {
                    GradeScope::Any
                } else {
                    GradeScope::Taught
                };
                competencies.push(Competency {
                    teacher_id: tid,
                    subject_id: subject_id(s),
                    role,
                    grade_scope: scope,
                });
            }
        }
        for e in &t.unavailable {
            unavailabilities.push(Unavailability {
                teacher_id: tid,
                exam_id: exam_id(e),
                reason: None,
            });
        }
    }
    Problem {
        school_year: SchoolYear {
            id: SchoolYearId(1),
            name: "2026-2027".to_string(),
            is_current: true,
        },
        campuses: inp
            .campuses
            .iter()
            .enumerate()
            .map(|(i, c)| Campus {
                id: CampusId(i as i64 + 1),
                code: c.clone(),
                name: c.clone(),
                color: format!("palette-{}", i + 1),
            })
            .collect(),
        grades: [10, 11, 12]
            .iter()
            .enumerate()
            .map(|(i, g)| Grade {
                id: GradeId(i as i64 + 1),
                code: *g,
                name: format!("Khối {g}"),
                sort_order: i as i32 + 1,
            })
            .collect(),
        subjects: vec![
            subject(1, "VL", "Vật lí", 2),
            subject(2, "CN", "Công nghệ", 1),
        ],
        teachers,
        teacher_grades,
        competencies,
        exams: EXAMS
            .iter()
            .enumerate()
            .map(|(i, (code, name))| Exam {
                id: ExamId(i as i64 + 1),
                school_year_id: SchoolYearId(1),
                code: code.to_string(),
                name: name.to_string(),
                sort_order: i as i32 + 1,
            })
            .collect(),
        unavailabilities,
        locks: Vec::new(),
        rule_settings: RuleSetting::default_settings(),
    }
}

fn manual_plan(inp: &Input) -> Vec<Assignment> {
    inp.manual_plan
        .iter()
        .map(|a| {
            let tid = inp
                .teachers
                .iter()
                .position(|t| t.code == a.teacher)
                .expect("teacher") as i64
                + 1;
            Assignment::new(
                ExamId(EXAMS.iter().position(|(c, _)| *c == a.exam).expect("exam") as i64 + 1),
                GradeId(match a.grade {
                    10 => 1,
                    11 => 2,
                    _ => 3,
                }),
                subject_id(&a.subject),
                TeacherId(tid),
                if a.role == "setter" {
                    Role::Setter
                } else {
                    Role::Reviewer
                },
                a.position,
            )
        })
        .collect()
}

fn label(k: RuleKey) -> &'static str {
    match k {
        RuleKey::S1 => "S1 Tần suất phản biện",
        RuleKey::S2 => "S2 Cân bằng vai trò",
        RuleKey::S3 => "S3 Độc lập cơ sở",
        RuleKey::S4 => "S4 Đa dạng cặp ra đề",
        RuleKey::S5 => "S5 Đa dạng quan hệ phản biện",
        RuleKey::S6 => "S6 Ra đề liên tiếp",
        RuleKey::S7 => "S7 Xoay vòng khối",
        RuleKey::S8 => "S8 Cân bằng khối lượng",
        RuleKey::S9 => "S9 Dồn việc trong kỳ",
        _ => "S10 Thiếu môn phản biện",
    }
}

fn rule_penalty(r: &ScoreReport, k: RuleKey) -> (f64, f64) {
    r.by_rule
        .iter()
        .find(|x| x.rule == k)
        .map_or((0.0, 0.0), |x| (x.units, x.penalty))
}

fn violation_summary(problem: &Problem, a: &[Assignment]) -> BTreeMap<String, usize> {
    let mut m = BTreeMap::new();
    for v in validate_assignments(problem, a, &ValidateOptions::default()) {
        *m.entry(v.code.clone()).or_insert(0) += 1;
    }
    m
}

fn load_by_teacher(inp: &Input, a: &[Assignment]) -> BTreeMap<String, usize> {
    let mut m: BTreeMap<String, usize> = inp.teachers.iter().map(|t| (t.code.clone(), 0)).collect();
    for x in a {
        if let Some(t) = inp.teachers.get((x.teacher_id.0 - 1) as usize) {
            *m.entry(t.code.clone()).or_insert(0) += 1;
        }
    }
    m
}

/// Min and max load among teachers who can set Vật lí, including those given no seat.
fn load_spread(inp: &Input, load: &BTreeMap<String, usize>) -> (usize, usize) {
    let v: Vec<usize> = inp
        .teachers
        .iter()
        .filter(|t| t.setter.iter().any(|s| s == "VL"))
        .map(|t| load[&t.code])
        .collect();
    (
        v.iter().copied().min().unwrap_or(0),
        v.iter().copied().max().unwrap_or(0),
    )
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let input_path = args
        .get(1)
        .expect("usage: site_comparison <input.json> [output_dir]");
    let out_dir = PathBuf::from(args.get(2).map_or("docs/reports/site3", String::as_str));
    fs::create_dir_all(&out_dir).expect("create output dir");
    let inp: Input = serde_json::from_str(&fs::read_to_string(input_path).expect("read input"))
        .expect("parse input");
    let problem = build_problem(&inp);
    let errs = problem.validate();
    if !errs.is_empty() {
        eprintln!("structural validation failed: {errs:?}");
        std::process::exit(1);
    }
    let feas = check_feasibility(&problem);
    let manual = manual_plan(&inp);
    let m_report = evaluate(&problem, &manual);
    let m_viol = violation_summary(&problem, &manual);

    let mut md = String::new();
    writeln!(
        md,
        "# Đo so sánh: phương án thủ công đã số hoá và ExamPanel\n"
    )
    .unwrap();
    writeln!(
        md,
        "> Tệp do `crates/service/examples/site_comparison.rs` sinh từ `{input_path}`; mọi con số do chương trình in ra. Giáo viên chỉ có mã GV01…, không có tên thật.\n"
    )
    .unwrap();
    writeln!(
        md,
        "- Quy mô: {} giáo viên, {} phân hiệu, 4 kỳ × 3 khối, {} vị trí trong phương án thủ công.",
        problem.teachers.len(),
        problem.campuses.len(),
        manual.len()
    )
    .unwrap();
    writeln!(
        md,
        "- Kiểm tra khả thi trước khi giải: **{}** ({} lỗi, {} cảnh báo).",
        if feas.is_feasible() {
            "KHẢ THI"
        } else {
            "KHÔNG KHẢ THI"
        },
        feas.errors.len(),
        feas.warnings.len()
    )
    .unwrap();
    for e in &feas.errors {
        writeln!(md, "  - Lỗi: `{}` {:?}", e.code, e.params).unwrap();
    }
    for w in &feas.warnings {
        writeln!(md, "  - Cảnh báo: `{}` {:?}", w.code, w.params).unwrap();
    }
    writeln!(md, "\n## Phương án thủ công: vi phạm ràng buộc cứng\n").unwrap();
    if m_viol.is_empty() {
        writeln!(md, "Không có vi phạm ràng buộc cứng.").unwrap();
    } else {
        writeln!(md, "| Mã vi phạm | Số lần |\n| :--- | :---: |").unwrap();
        for (c, n) in &m_viol {
            writeln!(md, "| `{c}` | {n} |").unwrap();
        }
    }

    let opts = OptimizeOptions {
        base_seed: BASE_SEED,
        num_runs: NUM_RUNS,
        budget: Budget::Iterations(ITERATIONS),
        max_plans: 3,
        diversity_threshold: 0.20,
        initial_assignments: None,
        cancel: None,
        progress: None,
    };
    let started = std::time::Instant::now();
    let result = optimize(&problem, &opts);
    let elapsed_ms = started.elapsed().as_millis();
    let mut scores = serde_json::json!({ "manual": m_report, "manual_hard_violations": m_viol });
    match result {
        Err(e) => {
            writeln!(
                md,
                "\n## ExamPanel\n\nBộ giải không tìm được phương án: `{e}`."
            )
            .unwrap();
            writeln!(
                md,
                "\nĐây là kết quả đúng với dữ liệu đầu vào; cần xem lại năng lực ra đề/phản biện hoặc hạn mức trong tệp đầu vào."
            )
            .unwrap();
        }
        Ok(r) => {
            let best = &r.plans[0];
            let o_viol = violation_summary(&problem, &best.assignments);
            writeln!(
                md,
                "\n## So sánh điểm phạt mềm S1–S10 (càng thấp càng tốt)\n\nTham số tối ưu: seed {BASE_SEED}, R = {NUM_RUNS}, {ITERATIONS} vòng/lần chạy; thời gian chạy {elapsed_ms} ms.\n"
            )
            .unwrap();
            writeln!(
                md,
                "| Quy tắc | Thủ công (đơn vị) | Thủ công (phạt) | ExamPanel (đơn vị) | ExamPanel (phạt) |\n| :--- | :---: | :---: | :---: | :---: |"
            )
            .unwrap();
            for k in [
                RuleKey::S1,
                RuleKey::S2,
                RuleKey::S3,
                RuleKey::S4,
                RuleKey::S5,
                RuleKey::S6,
                RuleKey::S7,
                RuleKey::S8,
                RuleKey::S9,
                RuleKey::S10,
            ] {
                let (mu, mp) = rule_penalty(&m_report, k);
                let (ou, op) = rule_penalty(&best.report, k);
                writeln!(
                    md,
                    "| {} | {mu:.2} | {mp:.2} | {ou:.2} | {op:.2} |",
                    label(k)
                )
                .unwrap();
            }
            writeln!(
                md,
                "| **Tổng** | | **{:.2}** | | **{:.2}** |",
                m_report.total, best.report.total
            )
            .unwrap();
            let red = if m_report.total.abs() > 1e-12 {
                (m_report.total - best.report.total) / m_report.total * 100.0
            } else {
                0.0
            };
            writeln!(md, "\n**Tỉ lệ giảm điểm phạt mềm: {red:.2}%.**\n").unwrap();
            writeln!(
                md,
                "Vi phạm ràng buộc cứng của phương án ExamPanel: {}.",
                if o_viol.is_empty() {
                    "không có".to_string()
                } else {
                    format!("{o_viol:?}")
                }
            )
            .unwrap();
            let m_load = load_by_teacher(&inp, &manual);
            let o_load = load_by_teacher(&inp, &best.assignments);
            writeln!(
                md,
                "\n## Khối lượng nhiệm vụ theo giáo viên (số vị trí, đếm trực tiếp từ bảng phân công)\n\n| Mã GV | Thủ công | ExamPanel |\n| :--- | :---: | :---: |"
            )
            .unwrap();
            for t in &inp.teachers {
                writeln!(
                    md,
                    "| {} | {} | {} |",
                    t.code, m_load[&t.code], o_load[&t.code]
                )
                .unwrap();
            }
            let (m_min, m_max) = load_spread(&inp, &m_load);
            let (o_min, o_max) = load_spread(&inp, &o_load);
            writeln!(
                md,
                "\nMax–Min nhóm Vật lí (loại giáo viên chỉ ra đề Công nghệ; tính cả giáo viên chưa được giao vị trí nào): thủ công {m_max} − {m_min} = {}; ExamPanel {o_max} − {o_min} = {}.",
                m_max - m_min,
                o_max - o_min
            )
            .unwrap();
            scores["load_by_teacher"] =
                serde_json::json!({ "manual": m_load, "optimized": o_load });
            scores["optimized"] = serde_json::json!(best.report);
            scores["optimized_hard_violations"] = serde_json::json!(o_viol);
            scores["reduction_percent"] = serde_json::json!(red);
            scores["optimizer_ms"] = serde_json::json!(elapsed_ms);
        }
    }
    fs::write(out_dir.join("site3_comparison.md"), &md).expect("write md");
    fs::write(
        out_dir.join("site3_scores.json"),
        serde_json::to_string_pretty(&scores).expect("scores"),
    )
    .expect("write scores");
    println!("{md}");
}
