<?php
// Get input values and sanitize them
$firstName = isset($_POST['firstName']) ? htmlspecialchars(trim($_POST['firstName'])) : '';
$lastName = isset($_POST['lastName']) ? htmlspecialchars(trim($_POST['lastName'])) : '';
$email = isset($_POST['email']) ? filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL) : '';
$comments = isset($_POST['comments']) ? htmlspecialchars(trim($_POST['comments'])) : '';

// Validate inputs (basic example)
if (empty($firstName) || empty($lastName) || empty($email) || empty($comments)) {
    die("All fields are required.");
}

// Validate email format
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    die("Invalid email format.");
}

// Database connection
$conn = new mysqli('localhost', 'root', '', 'test');

// Check connection
if ($conn->connect_error) {
    die("Connection Failed: " . $conn->connect_error);
}

// Prepare the SQL statement
$stmt = $conn->prepare("INSERT INTO personal (firstName, lastName, email, comments) VALUES (?, ?, ?, ?)");

// Check if the statement is prepared successfully
if (!$stmt) {
    die("Prepare failed: " . $conn->error);
}

// Bind parameters and execute the query
$stmt->bind_param("ssss", $firstName, $lastName, $email, $comments);

if ($stmt->execute()) {
    echo "Personal details have been submitted successfully!";
    echo '<br><br><button onclick="window.location.href=\'http://127.0.0.1:3000/index.html\'">Back to Home</button>';
} else {
    echo "Error: " . $stmt->error;
}

// Close connections
$stmt->close();
$conn->close();
?>