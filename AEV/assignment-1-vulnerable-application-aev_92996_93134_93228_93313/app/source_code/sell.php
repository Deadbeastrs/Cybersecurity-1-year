<?php
ini_set('display_startup_errors',1);
ini_set('display_errors',1);
error_reporting(-1);

session_start();
// session is not set
if( ! ($_SESSION["uid"] != NULL && $_SESSION["uid"] == "1")){
	header("location:index.php");
}
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>SELL</title>
		<link rel="stylesheet" href="css/bootstrap.min.css"/>
		<script src="js/jquery2.js"></script>
		<script src="js/bootstrap.min.js"></script>
		<script src="main.js"></script>
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
<body>
<div class="wait overlay">
	<div class="loader"></div>
</div>
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="container-fluid">	
			<div class="navbar-header">
				<a href="index.php" class="navbar-brand">Online Store</a>
			</div>
			<ul class="nav navbar-nav">
				<li><a href="index.php"><span class="glyphicon glyphicon-home"></span>Home</a></li>
				<li><a href="index.php"><span class="glyphicon glyphicon-modal-window"></span>Product</a></li>
				<li><a href="sell.php"><span class="glyphicon glyphicon-euro"></span>Sell</a></li>
                <li> <a href="customer_registration.php"><i class="fas fa-user-plus"></i>SignUp</a></li>
            </ul>
		</div>
	</div>
	<p><br/></p>
	<p><br/></p>
	<p><br/></p>
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-2"></div>
			<div class="col-md-8" id="signup_msg">
				<!--Alert from signup form-->
			</div>
			<div class="col-md-2"></div>
		</div>
		<div class="row">
			<div class="col-md-2"></div>
			<div class="col-md-8">
				<div class="panel panel-primary">
					<div class="panel-heading">Identify product to sell </div>
					<div class="panel-body">
					
					<form id="signup_form" onsubmit="return false">
						<div class="row">
							<div class="col-md-12">
								<label for="p_id">ID (ex:100,101...)</label>
								<input type="text" id="p_id" name="p_id" class="form-control">
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<label for="p_cat">Category (ex: [1,6])</label>
								<input type="text" id="p_cat" name="p_cat"class="form-control">
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<label for="p_brand">Brand (ex: [0,6])</label>
								<input type="text" id="p_brand" name="p_brand"class="form-control">
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<label for="p_title">Title (ex: Samsung, Apple)</label>
								<input type="text" id="p_title" name="p_title"class="form-control">
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<label for="p_price">Price</label>
								<input type="text" id="p_price" name="p_price"class="form-control">
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<label for="p_des">Description (ex: Samsung S21, Iphone X)</label>
								<input type="text" id="p_des" name="p_des"class="form-control">
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<label for="p_key">Keywords (ex: samsung mobile electronics, iphone apple mobile)</label>
								<input type="text" id="p_key" name="p_key"class="form-control">
							</div>
						</div>

						<label for="price">Image</label>
                        <input id="fileupload" type="file" name="fileupload"/>

                        
						<p><br/></p>
						<div class="row">
							<div class="col-md-12">
								<input style="width:100%;" onclick="uploadFile()"  value="Add" type="submit" id="add_product_button" name="add_product_button"class="btn btn-success btn-lg">
							</div>
						</div>
						
					</div>
					</form>
					<div class="panel-footer"></div>
				</div>
			</div>
			<div class="col-md-2"></div>
		</div>
	</div>
<script>
async function uploadFile() {
    let formData = new FormData();           
    formData.append("file", fileupload.files[0]);
    await fetch('/upload.php', {
    method: "POST", 
    body: formData
    }).then(
		function(response){
			if(response.status == 422){
				alert("ERROR");
			}else{
				alert("Approved");
			}
		}
	);    

}
</script>

</body>
</html>


















