from bs4 import BeautifulSoup
import httpx


def parse_table(table):
    table = BeautifulSoup(table, "html.parser")
    assignments = []

    for row in table.find_all("tr"):
        columns = row.find_all("td")
        campus = columns[1].text.strip()
        block = columns[2].text.strip()
        classroom = columns[3].text.strip()
        group = columns[4].text.strip()
        course = columns[6].text.strip()
        date = columns[8].text.strip()
        start_time = columns[10].text.strip()
        end_time = columns[11].text.strip()
        professor = columns[12].text.strip()
        starts_at = f"{date}T{start_time}-05:00"
        ends_at = f"{date}T{end_time}-05:00"

        assignments.append(
            {
                "campus": campus,
                "block": block,
                "classroom": classroom,
                "group": group,
                "course": course,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "professor": professor,
            }
        )
    return assignments


def get_student_schedule_table_html(student_id: str, start_date: str, end_date: str):
    data = {
        "actionID": "consultardatos",
        "Fecha_ini": start_date,
        "Fecha_Fin": end_date,
        "Num_Docente": "",
        "Num_Estudiante": student_id,
    }
    r = httpx.post(
        "https://artemisa.unbosque.edu.co/serviciosacademicos/EspacioFisico/Interfas/funcionesEspaciosFisicosAsigandosReporte.php",
        data=data,
    )
    if r.status_code == 200:
        return r.text
    else:
        return None
