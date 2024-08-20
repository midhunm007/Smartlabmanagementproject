<?php
$servername = "localhost"; // Change this to your server name
$username = "root"; // Change this to your MySQL username
$password = "password"; // Change this to your MySQL password
$database = "mydb"; // Change this to your MySQL database name

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully"; // Commented out to avoid displaying message in HTML

// Now $conn is your MySQL database connection object.

