import {
    getStudents,
    deleteStudent
} from "./localStorageOperations.js";

import {
    renderTable
} from "./displayOperations.js";


// Кнопка добавления студента

const addButton = document.querySelector(
    "#show-add-form-bin"
);

addButton.addEventListener("click", () => {
    location.href = "/html/studentFormPage.html";
});


// Элементы фильтра

const filterForm = document.querySelector(
    "#filter-form"
);

const groupFilter = document.querySelector(
    "#group-filter"
);

const dormitoryFilter = document.querySelector(
    "#dormitory-filter"
);

const resetFilterButton = document.querySelector(
    "#reset-filter-button"
);


// Загрузка студентов

async function loadStudents() {
    try {
        const students = await getStudents(
            groupFilter.value.trim(),
            dormitoryFilter.value.trim()
        );

        renderTable(undefined, students);

    } catch (error) {
        console.error(
            "Ошибка при загрузке студентов:",
            error
        );
    }
}


// Первоначальная загрузка

loadStudents();


// Обработка фильтрации

filterForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        await loadStudents();
    }
);


// Сброс фильтров

resetFilterButton.addEventListener(
    "click",
    async () => {
        groupFilter.value = "";
        dormitoryFilter.value = "";

        await loadStudents();
    }
);


// Работа с кнопками в таблице

const table = document.querySelector(
    "#students-tbody"
);

table.addEventListener(
    "click",
    async (event) => {
        const row = event.target.closest("tr");

        if (!row) {
            return;
        }

        const studentID = row.dataset.id;


        // Удаление студента

        if (
            event.target.classList.contains(
                "btn-delete"
            )
        ) {
            try {
                await deleteStudent(studentID);

                await loadStudents();

            } catch (error) {
                console.error(
                    "Ошибка при удалении студента:",
                    error
                );
            }
        }


        // Редактирование студента

        if (
            event.target.classList.contains(
                "btn-edit"
            )
        ) {
            location.href =
                `/html/studentFormPage.html?id=${studentID}`;
        }
    }
);