// Alumni functions
function openModalFromBtn(button) {
    document.getElementById('modal_company').value = button.getAttribute('data-company');
    document.getElementById('modal_designation').value = button.getAttribute('data-designation');
    document.getElementById('modal_passing_year').value = button.getAttribute('data-passingyear');
    document.getElementById('modal_whatsapp').value = button.getAttribute('data-whatsapp');
    document.getElementById('modal_job_duration').value = button.getAttribute('data-duration');
    document.getElementById('modal_previous_companies').value = button.getAttribute('data-previous');
    document.getElementById('modal_blood_group').value = button.getAttribute('data-bloodgroup');

    document.getElementById('editModal').classList.add('active');
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
}

function filterAlumni() {
    let searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    let input = searchInput.value.toLowerCase();
    let cards = document.getElementsByClassName('alumni-card');

    for (let i = 0; i < cards.length; i++) {
        let name = cards[i].querySelector('.search-name') ? cards[i].querySelector('.search-name').innerText.toLowerCase() : '';
        let desig = cards[i].querySelector('.search-desig') ? cards[i].querySelector('.search-desig').innerText.toLowerCase() : '';
        let comp = cards[i].querySelector('.search-comp') ? cards[i].querySelector('.search-comp').innerText.toLowerCase() : '';
        let batch = cards[i].querySelector('.search-batch') ? cards[i].querySelector('.search-batch').innerText.toLowerCase() : '';

        if (name.includes(input) || desig.includes(input) || comp.includes(input) || batch.includes(input)) {
            cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
    }
}

// Registration role toggle and datepicker
document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('role');
    const studentIdGroup = document.getElementById('student-id-group');
    const departmentGroup = document.getElementById('department-group');
    const passingYearGroup = document.getElementById('passing-year-group');

    const studentIdInput = document.getElementById('student_id');
    const departmentInput = document.getElementById('department');
    const passingYearInput = document.getElementById('passing_year');

    if (roleSelect && studentIdGroup && departmentGroup) {
        function toggleFields() {
            if (roleSelect.value === 'company') {
                studentIdGroup.style.display = 'none';
                departmentGroup.style.display = 'none';
                if (passingYearGroup) passingYearGroup.style.display = 'none';
                
                studentIdInput.required = false;
                departmentInput.required = false;
                if (passingYearInput) passingYearInput.required = false;

            } else if (roleSelect.value === 'alumni') {
                studentIdGroup.style.display = 'none';
                departmentGroup.style.display = 'block';
                if (passingYearGroup) passingYearGroup.style.display = 'block';

                studentIdInput.required = false;
                departmentInput.required = true;
                if (passingYearInput) passingYearInput.required = true;

            } else {
                studentIdGroup.style.display = 'block';
                departmentGroup.style.display = 'block';
                if (passingYearGroup) passingYearGroup.style.display = 'none';
                
                studentIdInput.required = true;
                departmentInput.required = true;
                if (passingYearInput) passingYearInput.required = false;
            }
        }

        roleSelect.addEventListener('change', toggleFields);
        toggleFields();
    }

    if (passingYearInput) {
        flatpickr("#passing_year", {
            dateFormat: "d/m/Y",
            allowInput: true
        });
    }
});
