
let productsOptions = '';

document.querySelectorAll(
    '.product-select option'
).forEach(option => {

    if (option.value !== '') {

        productsOptions += `
            <option
                value="${option.value}"
                data-name="${option.dataset.name}"
                data-hsn="${option.dataset.hsn}"
                data-gst="${option.dataset.gst}"
                data-rate="${option.dataset.rate}">

                ${option.text}

            </option>
        `;
    }
});


function addRow() {

    let tableBody = document.querySelector(
        '#invoice-table tbody'
    );

    let row = `

    <tr>

        <td>

            <select name="product[]"
                    class="form-control product-select"
                    required>

                <option value="">
                    Select Product
                </option>

                ${productsOptions}

            </select>

        </td>

        <td>

            <input type="text"
                name="hsn[]"
                class="form-control hsn"
                readonly>

        </td>

        <td>

            <input type="number"
                step="0.01"
                name="quantity[]"
                class="form-control quantity"
                required>

        </td>

        <td>

            <input type="number"
                step="0.01"
                name="rate[]"
                class="form-control rate"
                readonly>

        </td>

        <td>

            <input type="number"
                step="0.01"
                name="gst[]"
                class="form-control gst"
                readonly>

        </td>

        <td>

            <input type="number"
                class="form-control amount"
                readonly>

        </td>

        <td>

            <button type="button"
                    class="btn btn-danger"
                    onclick="removeRow(this)">

                X

            </button>

        </td>

    </tr>

    `;

    tableBody.insertAdjacentHTML(
        'beforeend',
        row
    );
}

document.addEventListener(
    'change',
    function(e) {

        if (
            e.target.classList.contains(
                'product-select'
            )
        ) {

            let selectedOption =
                e.target.options[
                    e.target.selectedIndex
                ];

            let row = e.target.closest('tr');

            let hsn =
                selectedOption.getAttribute(
                    'data-hsn'
                );

            let gst =
                selectedOption.getAttribute(
                    'data-gst'
                );

            let rate =
                selectedOption.getAttribute(
                    'data-rate'
                );

            row.querySelector('.hsn').value =
                hsn;

            row.querySelector('.gst').value =
                gst;

            row.querySelector('.rate').value =
                rate;

            calculateTotals();
        }
    }
);


function removeRow(button) {

    let row = button.closest('tr');

    row.remove();

    calculateTotals();
}


document.addEventListener(
    'input',
    function(e) {

        if (
            e.target.classList.contains('quantity')
            ||
            e.target.classList.contains('rate')
            ||
            e.target.classList.contains('gst')
            ||
            e.target.id === 'discount'
        ) {

            calculateTotals();
        }
    }
);


function calculateTotals() {

    let rows = document.querySelectorAll(
        '#invoice-table tbody tr'
    );

    let subtotal = 0;

    let totalGST = 0;

    rows.forEach(row => {

        let qty = parseFloat(
            row.querySelector('.quantity').value
        ) || 0;

        let rate = parseFloat(
            row.querySelector('.rate').value
        ) || 0;

        let gst = parseFloat(
            row.querySelector('.gst').value
        ) || 0;

        let amount = qty * rate;

        let gstAmount = (amount * gst) / 100;

        subtotal += amount;

        totalGST += gstAmount;

        row.querySelector('.amount').value =
            amount.toFixed(2);
    });

    let discount = parseFloat(
        document.getElementById('discount').value
    ) || 0;

    let grandTotal =
        subtotal + totalGST - discount;

    document.getElementById(
        'subtotal'
    ).innerText = subtotal.toFixed(2);

    document.getElementById(
        'gst-total'
    ).innerText = totalGST.toFixed(2);

    document.getElementById(
        'grand-total'
    ).innerText = grandTotal.toFixed(2);
}

function openActionModal(url, title, message) {

    document.getElementById(
        'actionModal'
    ).style.display = 'flex';

    document.getElementById(
        'actionModalTitle'
    ).innerText = title;

    document.getElementById(
        'actionModalMessage'
    ).innerText = message;

    document.getElementById(
        'actionModalConfirm'
    ).href = url;
}

function closeActionModal() {

    document.getElementById(
        'actionModal'
    ).style.display = 'none';
}