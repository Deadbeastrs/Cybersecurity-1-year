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