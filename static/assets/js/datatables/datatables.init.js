/*
Template Name: Tailwick - Admin & Dashboard Template
Author: Themesbrand
Version: 1.0.0
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Main Js File
*/

//basic example
new DataTable('#basic_tables');

//row Borders example
new DataTable('#rowBorder', {
    pageLength: 5,
});

//Hoverable example
new DataTable('#hoverableTable', {
    pageLength: 5,
});

//Hoverable example
new DataTable('#borderedTable', {
    pageLength: 5,
});

//Alternative pagination
new DataTable('#alternativePagination', {
    pagingType: 'full_numbers'
});

//Hidden columns
new DataTable('#hiddenColumns', {
    columnDefs: [
        {
            target: 2,
            visible: false,
            searchable: false
        },
        {
            target: 3,
            visible: false
        }
    ]
});

//add rows
function addNewRow() {
    table.row
        .add([
            counter + '.1',
            counter + '.2',
            counter + '.3',
            counter + '.4',
            counter + '.5'
        ])
        .draw(false);

    counter++;
}

const table = new DataTable('#example');
let counter = 1;

// Automatically add a first row of data
addNewRow();

//Show / hide columns dynamically

const tableDynamically = new DataTable('#tableDynamically', {
    pageLength: 5,
});

document.querySelectorAll('button.toggle-vis').forEach((el) => {
    el.addEventListener('click', function (e) {
        e.preventDefault();

        let columnIdx = e.target.getAttribute('data-column');
        let column = tableDynamically.column(columnIdx);

        // Toggle the visibility
        column.visible(!column.visible());
    });
});

//Row selection and deletion (single row)

const rowSelectionDeletion = new DataTable('#rowSelectionDeletion');

rowSelectionDeletion.on('click', 'tbody tr', (e) => {
    let classList = e.currentTarget.classList;

    if (classList.contains('selected')) {
        classList.remove('selected');
    }
    else {
        rowSelectionDeletion.rows('.selected').nodes().each((row) => row.classList.remove('selected'));
        classList.add('selected');
    }
});

// document.querySelector('#deleteButton').addEventListener('click', function () {
//     rowSelectionDeletion.row('.selected').remove().draw(false);
// });

//Custom filtering - range search
const minEl = document.querySelector('#min');
const maxEl = document.querySelector('#max');
const customFiltering = new DataTable('#customFiltering');

//File export
$(document).ready(function () {
    $('#fileExport').DataTable({
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'copy',
                className: 'transition-all duration-200 ease-linear text-slate-500 btn bg-slate-100 border-slate-100 hover:text-white hover:bg-slate-600 hover:border-slate-600 focus:text-white focus:bg-slate-600 focus:border-slate-600 focus:ring focus:ring-slate-100 active:text-white active:bg-slate-600 active:border-slate-600 active:ring active:ring-slate-100'
            },
            {
                extend: 'csv',
                className: 'transition-all duration-200 ease-linear text-slate-500 btn bg-slate-100 border-slate-100 hover:text-white hover:bg-slate-600 hover:border-slate-600 focus:text-white focus:bg-slate-600 focus:border-slate-600 focus:ring focus:ring-slate-100 active:text-white active:bg-slate-600 active:border-slate-600 active:ring active:ring-slate-100'
            },
            {
                extend: 'excel',
                className: 'transition-all duration-200 ease-linear text-slate-500 btn bg-slate-100 border-slate-100 hover:text-white hover:bg-slate-600 hover:border-slate-600 focus:text-white focus:bg-slate-600 focus:border-slate-600 focus:ring focus:ring-slate-100 active:text-white active:bg-slate-600 active:border-slate-600 active:ring active:ring-slate-100'
            },
            {
                extend: 'pdf',
                className: 'transition-all duration-200 ease-linear text-slate-500 btn bg-slate-100 border-slate-100 hover:text-white hover:bg-slate-600 hover:border-slate-600 focus:text-white focus:bg-slate-600 focus:border-slate-600 focus:ring focus:ring-slate-100 active:text-white active:bg-slate-600 active:border-slate-600 active:ring active:ring-slate-100'
            },
            {
                extend: 'print',
                className: 'transition-all duration-200 ease-linear text-slate-500 btn bg-slate-100 border-slate-100 hover:text-white hover:bg-slate-600 hover:border-slate-600 focus:text-white focus:bg-slate-600 focus:border-slate-600 focus:ring focus:ring-slate-100 active:text-white active:bg-slate-600 active:border-slate-600 active:ring active:ring-slate-100'
            }
        ]
    });
});