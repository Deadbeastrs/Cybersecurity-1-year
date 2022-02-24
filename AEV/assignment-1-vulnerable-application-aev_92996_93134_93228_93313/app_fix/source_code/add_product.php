<?php
include "db.php";

$p_id = $_POST["p_id"];
$p_cat = $_POST['p_cat'];
$p_brand = $_POST['p_brand'];
$p_title = $_POST['p_title'];
$p_price = $_POST['p_price'];
$p_des = $_POST['p_des'];
$p_key = $_POST['p_key'];
$p_img = $_POST['p_img'];

$p_id = htmlspecialchars($p_id, ENT_QUOTES, 'UTF-8');
$p_cat = htmlspecialchars($p_cat, ENT_QUOTES, 'UTF-8');
$p_brand = htmlspecialchars($p_brand, ENT_QUOTES, 'UTF-8');
$p_title = htmlspecialchars($p_title, ENT_QUOTES, 'UTF-8');
$p_price = htmlspecialchars($p_price, ENT_QUOTES, 'UTF-8');
$p_des = htmlspecialchars($p_des, ENT_QUOTES, 'UTF-8');
$p_key = htmlspecialchars($p_key, ENT_QUOTES, 'UTF-8');
$p_img = htmlspecialchars($p_img, ENT_QUOTES, 'UTF-8');

// session is not set
if( ! ($_SESSION["uid"] != NULL && $_SESSION["uid"] == "1")){
    	echo "
    	<div class='alert alert-warning'>
    	<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a><b>User does not have permission to execute this action!</b>
    	</div>
    	";
	  http_response_code(422);
  	  exit(0);
}

if (empty($p_id) || empty($p_cat)|| empty($p_brand)|| empty($p_title)|| empty($p_price)|| empty($p_des)|| empty($p_key)) {
    echo "
    <div class='alert alert-warning'>
    <a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a><b>PLease Fill all fields..!</b>
    </div>
    ";
    exit();
}

$sql = "INSERT INTO `products` (`product_id`, `product_cat`, `product_brand`, `product_title`, `product_price`, `product_desc`, `product_image`, `product_keywords`) 
    VALUES ('$p_id', '$p_cat', '$p_brand', '$p_title', '$p_price', '$p_des', '$p_img','$p_key')";
$run_query = mysqli_query($con,$sql);
if ($run_query) {
    echo "
    <div class='alert alert-success'>
    <a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a>
    <b>PRODUCT WAS ADDED...!!!</b>
    </div>
    ";
}

?>
