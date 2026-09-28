import {
    getStudentById,
    addStudent,
    updateStudent
} from "./localStorageOperations.js";

import { createStudent } from "./studentInitialization.js";


const form = document.querySelector("#student-form");
const formSection = document.querySelector("#form-section");


function showError(message) {
    const oldError = document.querySelector(".error-message");

    if (oldError) {
        oldError.remove();
    }

    const errorBlock = document.createElement("p");

    errorBlock.classList.add("error-message");
    errorBlock.textContent = message;

    formSection.prepend(errorBlock);
}


// =========================================================
// Создание нового студента
// =========================================================

async function createNewStudent() {
    const formData = new FormData(form);

    const student = createStudent(
        formData.get("stu-name"),
        formData.get("stu-group"),
        formData.get("stu-isu"),
        formData.get("stu-hostel"),
        formData.get("stu-room"),
        formData.get("stu-date"),
        formData.has("stu-foreign"),
        formData.get("stu-notes")
    );

    await addStudent(student);

    location.href = "/";
}


// =========================================================
// Редактирование существующего студента
// =========================================================

async function updateExistingStudent(studentID) {
    const student = await getStudentById(studentID);

    if (student === null) {
        showError("Студент не найден");
        return;
    }


    // Заполняем форму

    document.querySelector("#stu-name").value =
        student.fullName ?? "";

    document.querySelector("#stu-group").value =
        student.group ?? "";

    document.querySelector("#stu-isu").value =
        student.ISU ?? "";

    document.querySelector("#stu-hostel").value =
        student.dormNumber ?? "";

    document.querySelector("#stu-room").value =
        student.room ?? "";

    document.querySelector("#stu-date").value =
        student.dateArrived ?? "";

    document.querySelector("#stu-foreign").checked =
        student.isForeign ?? false;

    document.querySelector("#stu-notes").value =
        student.notes ?? "";


    document.querySelector("#form-title").textContent =
        "Редактирование студента";


    // Отправка изменений

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        try {
            const updatedStudent = createStudent(
                formData.get("stu-name"),
                formData.get("stu-group"),
                formData.get("stu-isu"),
                formData.get("stu-hostel"),
                formData.get("stu-room"),
                formData.get("stu-date"),
                formData.has("stu-foreign"),
                formData.get("stu-notes"),
                student.ID
            );

            await updateStudent(
                studentID,
                updatedStudent
            );

            location.href = "/";
        } catch (error) {
            console.error(error);
            showError(error.message);
        }
    });
}


// =========================================================
// Определяем режим страницы
// =========================================================

async function init() {
    const studentID =
        new URLSearchParams(location.search).get("id");


    // Нет id → создание

    if (!studentID) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            try {
                await createNewStudent();
            } catch (error) {
                console.error(error);
                showError(error.message);
            }
        });

        return;
    }


    // Есть id → редактирование

    try {
        await updateExistingStudent(studentID);
    } catch (error) {
        console.error(error);
        showError(error.message);
    }
}


init();