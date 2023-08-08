import httpx


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
