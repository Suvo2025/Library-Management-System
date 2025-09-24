const API_BASE = "http://127.0.0.1:8000";  // FastAPI backend

document.addEventListener("DOMContentLoaded", () => {
  // Initial loads
  loadBooks();
  loadUsers();
  loadTransactions();

  // Add event listeners for forms
  document.getElementById("book-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("book-title").value;
    const author = document.getElementById("book-author").value;
    const isbn = document.getElementById("book-isbn").value;

    try {
      const response = await fetch(`${API_BASE}/books/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, author, isbn })
      });

      if (response.ok) {
        showMessage("Book added successfully!", "success");
        loadBooks();
        e.target.reset();
      } else {
        const error = await response.json();
        showMessage(`Error: ${error.detail || 'Failed to add book'}`, "error");
      }
    } catch (error) {
      showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("user-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("user-name").value;
    const email = document.getElementById("user-email").value;

    try {
      const response = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email })
      });

      if (response.ok) {
        showMessage("User added successfully!", "success");
        loadUsers();
        e.target.reset();
      } else {
        const error = await response.json();
        showMessage(`Error: ${error.detail || 'Failed to add user'}`, "error");
      }
    } catch (error) {
      showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("issue-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user_id = parseInt(document.getElementById("issue-user-id").value);
    const book_id = parseInt(document.getElementById("issue-book-id").value);

    try {
      const res = await fetch(`${API_BASE}/transactions/issue/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, book_id })
      });

      if (res.ok) {
        showMessage("Book issued successfully!", "success");
        loadBooks();
        loadTransactions();
      } else {
        const error = await res.json();
        showMessage(`Error: ${error.detail || 'Book not available or invalid request'}`, "error");
      }
      e.target.reset();
    } catch (error) {
      showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("return-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const transaction_id = parseInt(document.getElementById("return-transaction-id").value);

    try {
      const res = await fetch(`${API_BASE}/transactions/${transaction_id}/return/`, {
        method: "PUT"
      });

      if (res.ok) {
        showMessage("Book returned successfully!", "success");
        loadBooks();
        loadTransactions();
      } else {
        const error = await res.json();
        showMessage(`Error: ${error.detail || 'Invalid transaction or already returned'}`, "error");
      }
      e.target.reset();
    } catch (error) {
      showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("update-book-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const book_id = document.getElementById("update-book-id").value;
    const title = document.getElementById("update-book-title").value || undefined;
    const author = document.getElementById("update-book-author").value || undefined;
    const isbn = document.getElementById("update-book-isbn").value || undefined;
    
    const body = {};
    if (title) body.title = title;
    if (author) body.author = author;
    if (isbn) body.isbn = isbn;

    try {
        const response = await fetch(`${API_BASE}/books/${book_id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            showMessage("Book updated successfully!", "success");
            loadBooks();
            e.target.reset();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.detail || 'Failed to update book'}`, "error");
        }
    } catch (error) {
        showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("delete-book-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const book_id = document.getElementById("delete-book-id").value;

    try {
        const response = await fetch(`${API_BASE}/books/${book_id}`, {
            method: "DELETE"
        });

        if (response.ok) {
            showMessage("Book deleted successfully!", "success");
            loadBooks();
            e.target.reset();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.detail || 'Failed to delete book'}`, "error");
        }
    } catch (error) {
        showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("update-user-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user_id = document.getElementById("update-user-id").value;
    const name = document.getElementById("update-user-name").value || undefined;
    const email = document.getElementById("update-user-email").value || undefined;

    const body = {};
    if (name) body.name = name;
    if (email) body.email = email;

    try {
        const response = await fetch(`${API_BASE}/users/${user_id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            showMessage("User updated successfully!", "success");
            loadUsers();
            e.target.reset();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.detail || 'Failed to update user'}`, "error");
        }
    } catch (error) {
        showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  document.getElementById("delete-user-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user_id = document.getElementById("delete-user-id").value;

    try {
        const response = await fetch(`${API_BASE}/users/${user_id}`, {
            method: "DELETE"
        });

        if (response.ok) {
            showMessage("User deleted successfully!", "success");
            loadUsers();
            e.target.reset();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.detail || 'Failed to delete user'}`, "error");
        }
    } catch (error) {
        showMessage("Network error. Make sure the server is running.", "error");
    }
  });

  // Event listeners for details view
  document.getElementById("book-list").addEventListener("click", async (e) => {
    if (e.target.tagName === 'LI') {
      const bookId = e.target.getAttribute('data-id');
      if (bookId) {
        await showBookDetails(bookId);
      }
    }
  });

  document.getElementById("user-list").addEventListener("click", async (e) => {
    if (e.target.tagName === 'LI') {
      const userId = e.target.getAttribute('data-id');
      if (userId) {
        await showUserDetails(userId);
      }
    }
  });

  // Event listener for the toggle button.
  document.getElementById("book-list").addEventListener("click", async (e) => {
    if (e.target.classList.contains('toggle-btn')) {
        const bookId = e.target.getAttribute('data-id');
        try {
            const res = await fetch(`${API_BASE}/books/${bookId}/toggle-availability`, {
                method: "PUT"
            });
            if (res.ok) {
                showMessage("Book availability updated.", "success");
                loadBooks();
            } else {
                const error = await res.json();
                showMessage(`Error: ${error.detail || 'Failed to update availability'}`, "error");
            }
        } catch (error) {
            showMessage("Network error.", "error");
        }
    }
  });
});

// Load Books
async function loadBooks() {
    const query = document.getElementById("book-search").value;
    const sortBy = document.getElementById("book-sort").value;
    const url = new URL(`${API_BASE}/books/`);
    if (query) {
        url.searchParams.append('query', query);
    }
    if (sortBy) {
        url.searchParams.append('sort_by', sortBy);
    }

    try {
        const res = await fetch(url.toString());
        const books = await res.json();

        const list = document.getElementById("book-list");
        list.innerHTML = "";
        
        if (books.length === 0) {
            list.innerHTML = "<li>No books found</li>";
            return;
        }

        books.forEach(b => {
            const li = document.createElement("li");
            li.textContent = `[${b.id}] ${b.title} by ${b.author} (ISBN: ${b.isbn}) - ${b.available ? "Available ✅" : "Borrowed ❌"}`;
            li.setAttribute('data-id', b.id);
            const toggleBtn = document.createElement("button");
            toggleBtn.textContent = b.available ? "Mark as Borrowed" : "Mark as Available";
            toggleBtn.className = "toggle-btn";
            toggleBtn.setAttribute('data-id', b.id);
            li.appendChild(toggleBtn);
            list.appendChild(li);
        });
    } catch (error) {
        document.getElementById("book-list").innerHTML = "<li class='error'>Error loading books</li>";
    }
}

// Load Users
// Modify loadUsers to add the "View History" button
async function loadUsers() {
    const query = document.getElementById("user-search").value;
    const url = new URL(`${API_BASE}/users/`);
    if (query) {
        url.searchParams.append('query', query);
    }
    try {
        const res = await fetch(url.toString());
        const users = await res.json();
        const list = document.getElementById("user-list");
        list.innerHTML = "";
        if (users.length === 0) {
            list.innerHTML = "<li>No users found</li>";
            return;
        }
        users.forEach(u => {
            const li = document.createElement("li");
            const historyBtn = document.createElement("button");
            historyBtn.textContent = "View History";
            historyBtn.className = "history-btn";
            historyBtn.setAttribute('data-id', u.id);
            li.textContent = `[${u.id}] ${u.name} (${u.email})`;
            li.setAttribute('data-id', u.id);
            li.appendChild(historyBtn);
            list.appendChild(li);
        });
    } catch (error) {
        document.getElementById("user-list").innerHTML = "<li class='error'>Error loading users</li>";
    }
}

// Add this new event listener inside the DOMContentLoaded block
document.getElementById("user-list").addEventListener("click", async (e) => {
    if (e.target.classList.contains('history-btn')) {
        const userId = e.target.getAttribute('data-id');
        await showUserTransactionHistory(userId);
    }
});

// Add this new function
async function showUserTransactionHistory(userId) {
    try {
        const res = await fetch(`${API_BASE}/users/${userId}/transactions/`);
        if (res.ok) {
            const transactions = await res.json();
            if (transactions.length === 0) {
                alert("This user has no transaction history.");
                return;
            }
            let historyText = `User ${userId} Transaction History:\n\n`;
            transactions.forEach(t => {
                const statusText = t.status === "borrowed" && new Date(t.due_date) < new Date() ? "OVERDUE" : t.status;
                historyText += ` - Book ID: ${t.book_id}, Status: ${statusText} (Transaction ID: ${t.id})\n`;
            });
            alert(historyText);
        } else {
            const error = await res.json();
            showMessage(`Error: ${error.detail || 'Failed to fetch transaction history'}`, "error");
        }
    } catch (error) {
        showMessage("Network error.", "error");
    }
}
// Load Transactions
// Modify loadTransactions
async function loadTransactions() {
    const query = document.getElementById("transaction-search").value;
    const url = query ? `${API_BASE}/transactions/?query=${query}` : `${API_BASE}/transactions/`;

    try {
        const res = await fetch(url);
        const transactions = await res.json();
        const list = document.getElementById("transaction-list");
        list.innerHTML = "";
        
        if (transactions.length === 0) {
            list.innerHTML = "<li>No transactions found</li>";
            return;
        }

        const now = new Date();
        transactions.forEach(t => {
            const li = document.createElement("li");
            let statusText = `Status: ${t.status}`;
            const dueDate = t.due_date ? new Date(t.due_date) : null;
            
            if (t.status === "borrowed" && dueDate && dueDate < now) {
                statusText = `Status: ${t.status} - OVERDUE! 🔴`;
                li.style.backgroundColor = "#ffebeb"; // Highlight overdue items
                li.style.borderColor = "#d32f2f";
            }
            
            li.textContent = `[${t.id}] User ${t.user_id} - Book ${t.book_id} - ${statusText} (Due: ${dueDate ? dueDate.toLocaleDateString() : 'N/A'})`;
            list.appendChild(li);
        });
    } catch (error) {
        document.getElementById("transaction-list").innerHTML = "<li class='error'>Error loading transactions</li>";
    }
}

// Show success/error messages
function showMessage(message, type) {
  const existingMessage = document.querySelector('.message');
  if (existingMessage) {
    existingMessage.remove();
  }
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = message;
  document.body.insertBefore(messageDiv, document.body.firstChild);
  setTimeout(() => {
    messageDiv.remove();
  }, 5000);
}

// Function to fetch and display book details.
async function showBookDetails(bookId) {
    try {
        const res = await fetch(`${API_BASE}/books/${bookId}`);
        if (res.ok) {
            const book = await res.json();
            alert(`Book Details:\n\nTitle: ${book.title}\nAuthor: ${book.author}\nISBN: ${book.isbn}\nAvailable: ${book.available ? 'Yes' : 'No'}`);
        } else {
            showMessage("Book not found.", "error");
        }
    } catch (error) {
        showMessage("Error fetching book details.", "error");
    }
}

// Function to fetch and display user details.
async function showUserDetails(userId) {
    try {
        const res = await fetch(`${API_BASE}/users/${userId}`);
        if (res.ok) {
            const user = await res.json();
            alert(`User Details:\n\nName: ${user.name}\nEmail: ${user.email}`);
        } else {
            showMessage("User not found.", "error");
        }
    } catch (error) {
        showMessage("Error fetching user details.", "error");
    }
}