const API_URL = "/api/requests";


// Получение списка студентов
// GET /api/requests
// GET /api/requests?group=P3223&dormitory=8
async function getStudents(groupFilter = "", dormFilter = "") {
    const params = new URLSearchParams();

    if (groupFilter) {
        params.set("group", groupFilter);
    }

    if (dormFilter) {
        params.set("dormitory", dormFilter);
    }

    const query = params.toString();
    const url = query ? `${API_URL}?${query}` : API_URL;

    const response = await fetch(url);

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || `Ошибка HTTP: ${response.status}`);
    }

    return result;
}


// Получение одного студента
// GET /api/requests/:id
async function getStudentById(studentID) {
    const response = await fetch(
        `${API_URL}/${encodeURIComponent(studentID)}`
    );

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || `Ошибка HTTP: ${response.status}`);
    }

    return result;
}


// Добавление студента
// POST /api/requests
async function addStudent(student) {
    const response = await fetch(API_URL, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(student)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || `Ошибка HTTP: ${response.status}`);
    }

    return result;
}


// Изменение студента
// PATCH /api/requests/:id
async function updateStudent(studentID, student) {
    const response = await fetch(
        `${API_URL}/${encodeURIComponent(studentID)}`,
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(student)
        }
    );

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || `Ошибка HTTP: ${response.status}`);
    }

    return result;
}


// Удаление студента
// DELETE /api/requests/:id
async function deleteStudent(studentID) {
    const response = await fetch(
        `${API_URL}/${encodeURIComponent(studentID)}`,
        {
            method: "DELETE"
        }
    );

    if (!response.ok) {
        let result = {};

        try {
            result = await response.json();
        } catch {
            // Ответ может быть пустым
        }

        throw new Error(
            result.error || `Ошибка HTTP: ${response.status}`
        );
    }

    return true;
}


export {
    getStudents,
    getStudentById,
    addStudent,
    updateStudent,
    deleteStudent
};