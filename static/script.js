function registerLink(event){
    event.preventDefault(); // Ngăn chặn hành động mặc định của liên kết
    document.querySelector(".container_").classList.add("blur"); // Làm mờ biểu mẫu đăng nhập
    document.querySelector(".register").style.display = "block"; // Hiển thị biểu mẫu đăng ký
}
