function validateStudentForm(student) {
    let errorName = "";

    const names = student.fullName.trim().split(/\s+/);


    // Проверка ФИО

    if (
        student.fullName.trim() === "" ||
        names.length < 2 ||
        names.some((word) => word.length < 2)
    ) {
        errorName += "fullname ";
    }


    // Проверка группы

    const groupRegex = /^[A-Za-z]\d{4}$/;

    if (!groupRegex.test(student.group)) {
        errorName += "group ";
    }


    // Проверка ИСУ

    if (!/^[0-9]{6}$/.test(student.ISU)) {
        errorName += "ISU ";
    }


    if (errorName.length > 0) {
        throw new Error(errorName + "error");
    }


    // Если общежитие не указано,
    // комната и дата заселения тоже не используются

    if (String(student.dormNumber ?? "").trim() === "") {
        student.dormNumber = null;
    }

    if (
        String(student.dateArrived ?? "").trim() === "" ||
        student.dormNumber === null
    ) {
        student.dateArrived = null;
        student.room = null;
    }
}


function createStudent(
    fullName,
    group,
    ISU,
    dormNumber,
    stuRoom,
    dateArrived,
    isForeign,
    notes,
    id = null
) {
    const student = {
        fullName: fullName,
        group: group,
        ISU: ISU,
        dormNumber:
            dormNumber === "" ? null : Number(dormNumber),
        room:
            stuRoom === "" ? null : Number(stuRoom),
        dateArrived: dateArrived || null,
        isForeign: Boolean(isForeign),
        notes: notes || ""
    };


    // Уникальный ID ресурса

    student.ID = id ?? crypto.randomUUID();


    // Клиентская валидация

    validateStudentForm(student);


    // Нормализация ФИО

    const names = student.fullName
        .trim()
        .split(/\s+/);

    for (let i = 0; i < names.length; i++) {
        names[i] =
            names[i][0].toUpperCase() +
            names[i].slice(1).toLowerCase();
    }


    // Нормализация группы

    student.group =
        student.group[0].toUpperCase() +
        student.group.slice(1);


    student.fullName = names.join(" ");


    return student;
}


export { createStudent };