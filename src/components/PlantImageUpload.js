import React, { useState, useEffect } from 'react';

function PlantImageUpload({ file: externalFile, onFileChange }) {
    const [filePreview, setFilePreview] = useState(
        'https://via.placeholder.com/300x200.png?text=Plant+Image'
    );

    useEffect(() => {
        if (externalFile) {
            onFileChange(externalFile);
            const reader = new FileReader();
            reader.onloadend = () => {
                setFilePreview(reader.result);
            };
            reader.readAsDataURL(externalFile);
        }
    }, [externalFile]);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile || !selectedFile instanceof File) {
            // 파일이 없거나 파일이 아닌 경우에는 처리하지 않음
            return;
        }
        onFileChange(selectedFile); // 부모 컴포넌트로 파일 변경을 전달

        const reader = new FileReader();
        reader.onloadend = () => {
            setFilePreview(reader.result);
        };
        reader.readAsDataURL(selectedFile);
    };

    return (
        <div className="mb-4">
            <div className="w-full flex justify-center mb-5">
                {filePreview && (
                    <img
                        src={filePreview}
                        alt="미리보기"
                        className=" size-60  object-cover"
                    />
                )}
            </div>
            <input
                type="file"
                name="image"
                onChange={handleFileChange}
                className="mt-1 block w-full text-sm text-gray-500
                   file:mr-4 file:py-2 file:px-4
                   file:rounded-full file:border-0
                   file:text-sm file:font-semibold
                   file:bg-blue-50 file:text-blue-700
                   hover:file:bg-blue-100"
            />
        </div>
    );
}

export default PlantImageUpload;
