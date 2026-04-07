document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const resultSection = document.getElementById('result-section');
    const uploadSection = document.querySelector('.upload-section');
    const imagePreview = document.getElementById('image-preview');
    const resetBtn = document.getElementById('reset-btn');
    const loadingSpinner = document.getElementById('loading-spinner');

    // UI 엘리먼트
    const resPrediction = document.getElementById('res-prediction');
    const resCategory = document.getElementById('res-category');
    const resStyle = document.getElementById('res-style');
    const resTime = document.getElementById('res-time');

    // 클릭 시 파일 선택창 열기
    dropZone.addEventListener('click', () => fileInput.click());

    // 파일 선택 이벤트
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleUpload(e.target.files[0]);
        }
    });

    // 드래그 앤 드롭 이벤트
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('active');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('active');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleUpload(files[0]);
        }
    });

    // 업로드 및 분석 처리
    async function handleUpload(file) {
        if (!file.type.startsWith('image/')) {
            alert('이미지 파일만 업로드 가능합니다.');
            return;
        }

        // 미리보기 설정
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // UI 전환
        uploadSection.classList.add('hidden');
        resultSection.classList.remove('hidden');
        loadingSpinner.textContent = 'AI 분석 중...';
        resetResults();

        // API 호출
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/v1/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('서버 분석에 실패했습니다.');

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error(error);
            loadingSpinner.textContent = '오류 발생';
            alert('분석 중 오류가 발생했습니다: ' + error.message);
        }
    }

    function displayResults(data) {
        loadingSpinner.textContent = '분석 완료';
        resPrediction.textContent = data.prediction || '-';
        resCategory.textContent = data.category || '알 수 없음';
        resStyle.textContent = data.style || 'Casual';
        resTime.textContent = data.process_time || '0s';
    }

    function resetResults() {
        resPrediction.textContent = '-';
        resCategory.textContent = '-';
        resStyle.textContent = '-';
        resTime.textContent = '-';
    }

    // 초기화
    resetBtn.addEventListener('click', () => {
        uploadSection.classList.remove('hidden');
        resultSection.classList.add('hidden');
        fileInput.value = '';
    });
});
