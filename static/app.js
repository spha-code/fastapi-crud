// Configuration
const API_BASE_URL = '/api/items';

// DOM elements
const itemsList = document.getElementById('itemsList');
const loading = document.getElementById('loading');
const message = document.getElementById('message');
const formTitle = document.getElementById('formTitle');
const cancelBtn = document.getElementById('cancelBtn');
const itemIdInput = document.getElementById('itemId');

// Show message
function showMessage(msg, isError = false) {
    message.textContent = msg;
    message.className = isError ? 'error' : 'success';
    setTimeout(() => {
        message.textContent = '';
        message.className = '';
    }, 3000);
}

// Fetch all items
async function fetchItems() {
    loading.style.display = 'block';
    itemsList.innerHTML = '';

    try {
        const response = await fetch(API_BASE_URL);
        if (!response.ok) throw new Error('Failed to fetch items');

        const items = await response.json();

        loading.style.display = 'none';

        if (items.length === 0) {
            itemsList.innerHTML = '<p>No items found. Create your first item!</p>';
            return;
        }

        items.forEach(item => {
            const itemCard = createItemCard(item);
            itemsList.appendChild(itemCard);
        });
    } catch (error) {
        loading.style.display = 'none';
        showMessage('Error loading items: ' + error.message, true);
    }
}

// Create item card element
function createItemCard(item) {
    const card = document.createElement('div');
    card.className = 'item-card';

    const title = document.createElement('h3');
    title.textContent = item.name;

    const description = document.createElement('p');
    description.textContent = item.description || 'No description';

    const status = document.createElement('p');
    status.innerHTML = `<strong>Status:</strong> ${item.completed ? 'Completed ✓' : 'Pending'}`;

    const actions = document.createElement('div');
    actions.className = 'item-actions';

    const editBtn = document.createElement('button');
    editBtn.textContent = 'Edit';
    editBtn.onclick = () => editItem(item);

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'delete';
    deleteBtn.onclick = () => deleteItem(item.id);

    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    card.appendChild(title);
    card.appendChild(description);
    card.appendChild(status);
    card.appendChild(actions);

    return card;
}

// Save item (create or update)
async function saveItem() {
    const id = itemIdInput.value;
    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    const completed = document.getElementById('completed').checked;

    if (!name) {
        showMessage('Name is required', true);
        return;
    }

    const itemData = { name, description, completed };

    try {
        let response;
        if (id) {
            // Update existing item
            response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData),
            });
        } else {
            // Create new item
            response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData),
            });
        }

        if (!response.ok) throw new Error('Failed to save item');

        resetForm();
        fetchItems();
        showMessage(id ? 'Item updated successfully!' : 'Item created successfully!');
    } catch (error) {
        showMessage('Error saving item: ' + error.message, true);
    }
}

// Edit item
function editItem(item) {
    document.getElementById('itemId').value = item.id;
    document.getElementById('name').value = item.name;
    document.getElementById('description').value = item.description || '';
    document.getElementById('completed').checked = item.completed;

    formTitle.textContent = 'Edit Item';
    cancelBtn.classList.remove('hidden');
}

// Reset form
function resetForm() {
    document.getElementById('itemId').value = '';
    document.getElementById('name').value = '';
    document.getElementById('description').value = '';
    document.getElementById('completed').checked = false;

    formTitle.textContent = 'Create New Item';
    cancelBtn.classList.add('hidden');
}

// Delete item
async function deleteItem(id) {
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) throw new Error('Failed to delete item');

        fetchItems();
        showMessage('Item deleted successfully!');
    } catch (error) {
        showMessage('Error deleting item: ' + error.message, true);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', fetchItems);