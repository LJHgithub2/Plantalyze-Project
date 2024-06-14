import React from 'react';

function NumberInputWithButtons({ value, onChange, step, min, max, name }) {
    const handleIncrement = () => {
        if (max === undefined || value + step <= max) {
            onChange(value + step);
        }
    };

    const handleDecrement = () => {
        if (min === undefined || value - step >= min) {
            onChange(value - step);
        }
    };

    return (
        <div className="flex items-center mt-1">
            <button
                type="button"
                onClick={handleDecrement}
                className="px-3 py-2 bg-gray-200 text-gray-700 rounded-l-md focus:outline-none hover:bg-gray-300"
            >
                -
            </button>
            <input
                type="number"
                value={value}
                readOnly
                name={name} // 이름을 추가합니다.
                className="w-full px-3 py-2 border-t border-b border-gray-300 text-center focus:outline-none"
            />
            <button
                type="button"
                onClick={handleIncrement}
                className="px-3 py-2 bg-gray-200 text-gray-700 rounded-r-md focus:outline-none hover:bg-gray-300"
            >
                +
            </button>
        </div>
    );
}

export default NumberInputWithButtons;
