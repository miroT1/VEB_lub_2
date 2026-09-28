import { getStudentById } from "./localStorageOperations.js";


const studentID = new URLSearchParams(location.search).get("id");

const infoBody = document.querySelector("#student-info");


async function loadStudent() {
    if (!studentID) {
        infoBody.textContent = "ID студента не указан";
        return;
    }

    try {
        const student = await getStudentById(studentID);

        if (!student) {
            infoBody.textContent = "Студент не найден";
            return;
        }

        infoBody.innerHTML = `
            <p><strong>ФИО:</strong> ${student.fullName}</p>

            <p><strong>Группа:</strong> ${student.group}</p>

            <p><strong>ИСУ ID:</strong> ${student.ISU}</p>

            <p><strong>Общежитие:</strong> ${student.dormNumber ?? "-"}</p>

            <p><strong>Комната:</strong> ${student.room ?? "-"}</p>

            <p><strong>Дата заселения:</strong> ${student.dateArrived ?? "-"}</p>

            <p><strong>Иностранец:</strong> ${student.isForeign ? "Да" : "Нет"}</p>

            <p><strong>Заметки:</strong> ${student.notes || "-"}</p>

            <p><strong>ID:</strong> ${student.ID}</p>
        `;
    } catch (error) {
        console.error("Ошибка при загрузке студента:", error);

        infoBody.textContent =
            "Не удалось получить данные о студенте";
    }
}


loadStudent();