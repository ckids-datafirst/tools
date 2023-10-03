import sqlite3 as sqlite
from pathlib import Path


def open_database(database_file: Path) -> sqlite.Connection:
    """Open the database"""
    conn = sqlite.connect(database_file)
    return conn


def get_cursor(conn: sqlite.Connection) -> sqlite.Cursor:
    """Get a cursor for the database"""
    return conn.cursor()


def close_database(conn: sqlite.Connection):
    """Close the database"""
    conn.close()


def get_projects_by_semester(
    cursor: sqlite.Cursor, semester: str, year: str
) -> list[dict[str, str]]:
    """Get all projects"""
    cursor.execute(
        "SELECT id, name from project where year = ? and semester like ?",
        [year, semester],
    )
    results = cursor.fetchall()
    print(results)
    projects: list[dict[str, str]] = []
    for result in results:
        projects.append({"id": result[0], "name": result[1]})
    return projects


def get_students_by_semester(
    cursor: sqlite.Cursor, semester: str, year: str
) -> list[dict[str, str | None]]:
    """Get all students by semester"""
    cursor.execute(
        """
SELECT student.name, github_username from student
INNER JOIN project_has_student ON project_has_student.student_id = student.id
INNER JOIN project ON project.id = project_has_student.project_id
WHERE project.semester like ? and project.year = ?
""",
        [semester, year],
    )
    results = cursor.fetchall()

    students: list[dict[str, str | None]] = []
    for result in results:
        students.append({"name": result[0], "github_username": result[1]})
    return students


def get_members_of_team(cursor: sqlite.Cursor, project_id: str) -> list[str]:
    """Get all members of a team"""
    cursor.execute(
        "SELECT github_username from student INNER JOIN project_has_student ON project_has_student.student_id = student.id WHERE project_has_student.project_id = ? AND student.github_username IS NOT NULL;",
        [project_id],
    )
    return [row[0] for row in cursor.fetchall()]
