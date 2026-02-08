function analyzeImage() {
    const input = document.getElementById("imageInput");
    const result = document.getElementById("result");

    if (input.files.length === 0) {
        alert("กรุณาเลือกรูป");
        return;
    }

    const formData = new FormData();
    formData.append("image", input.files[0]);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            result.innerHTML = "❌ " + data.error;
        } else {
            result.innerHTML =
                "🟤 สีน้ำตาล: <b>" + data.brown_percent + "%</b>";
        }
    })
    .catch(err => {
        result.innerHTML = "เกิดข้อผิดพลาด";
        console.error(err);
    });
}
