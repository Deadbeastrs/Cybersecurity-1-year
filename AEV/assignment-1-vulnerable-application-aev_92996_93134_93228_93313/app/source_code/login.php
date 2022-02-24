<?php
include "db.php";

session_start ();

// login 

if(isset($_POST["userLogin"])){
    $email = mysqli_real_escape_string ($con, $_POST["userEmail"]);
    $password = hash('sha1', $_POST["userPassword"]);

    $sql = "SELECT user_id,first_name,password FROM user_info WHERE email='$email'";
    $run_query = mysqli_query($con,$sql);
    $row= mysqli_fetch_array($run_query);
    $sha1pass = $row["password"];

    if($password == $sha1pass)
    {
        $_SESSION["uid"] = $row["user_id"]; 
        $_SESSION["name"] = $row["first_name"];
        //header("location:profile.php");
        echo "loginsuccess";
    }
}
?>