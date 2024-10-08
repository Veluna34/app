<?php
// db.php

$host = 'sql1.njit.edu'; // Your database host
$db = 'Account Information'; // Your database name
$user = 'aaf45'; // Your database username
$pass = 'AFiggy123!'; // Your database password

// Create a connection
$conn = new mysqli($host, $user, $pass, $db);