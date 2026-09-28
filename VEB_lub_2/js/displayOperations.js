//! Отображение списка студентов

function renderTable(
    table = document.querySelector("tbody"),
    students = []
) {
    table.innerHTML = "";

    for (let i = 0; i < students.length; i++) {
        const template = `
            <tr data-id="${students[i].ID}">
                <td>
                    <a href="/html/infoPage.html?id=${students[i].ID}">
                        ${students[i].fullName}
                    </a>
                </td>

                <td>${students[i].group}</td>

                <td>${students[i].ISU}</td>

                <td>
                    <button class="btn-edit">Изменить</button>
                    <button class="btn-delete">Удалить</button>
                </td>
            </tr>
        `;

        table.innerHTML += template;
    }
}

export { renderTable };