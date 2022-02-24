
<?php

$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

/* Get the name of the uploaded file */
$filename = $_FILES['file']['name'];

/* Choose where to save the uploaded file */
$location = "uploads/".$filename;

if((strpos($filename, "jpg") == false && strpos($filename, "png") == false && strpos($filename, "jpeg") == false)){
  echo "Sorry, only JPG, JPEG, PNG files are allowed.";
  http_response_code(422);
  exit(0);
}

/* Save the uploaded file to the local filesystem */
if ( move_uploaded_file($_FILES['file']['tmp_name'], $location) ) { 
  echo 'Success'; 
} else { 
  echo 'Failure'; 
}

$checkf = mime_content_type($location);

if((strpos($checkf, "jpg") == false && strpos($checkf, "png") == false && strpos($checkf, "jpeg") == false)){
  echo "------\n";
  echo var_dump($checkf);
  echo "\n------\n";
  echo "Sorry,file type is not supported.";
  unlink($location);
  http_response_code(422);
  exit(0);
}

$array = explode(".", $filename);
$result = count($array);

if((strcmp($array[$result-1], "jpg") != 0 && strcmp($array[$result-1], "png") != 0 && strcmp($array[$result-1], "jpeg") != 0)){
  echo "------\n";
  echo var_dump($checkf);
  echo "\n------\n";
  echo "Sorry,file type is not supported.";
  unlink($location);
  http_response_code(422);
  exit(0);
}
?>