import React, { useId } from "react";

function InputBox({
    label,                  // "From" or "To"
    amount,                 // The number value
    onAmountChange,         // Function to handle number typing
    onCurrencyChange,       // Function to handle dropdown selection
    currencyOptions = [],   // Array of currencies (["usd", "eur", ...])
    selectCurrency = "usd", // The currently selected currency
    amountDisable = false,  // Optional: to lock the input
    currencyDisable = false, // Optional: to lock the dropdown
    className = "",         // Extra styling from parent
}) {
    // Generates a unique ID for accessibility (labels linked to inputs)
    const amountInputId = useId();

    return (
        <div className={`bg-white p-3 rounded-lg text-sm flex ${className}`}>
            {/* Left Side: Amount Input */}
            <div className="w-1/2">
                <label htmlFor={amountInputId} className="text-black/40 mb-2 inline-block">
                    {label}
                </label>
                <input
                    id={amountInputId}
                    className="outline-none w-full bg-transparent py-1.5"
                    type="number"
                    placeholder="Amount"
                    disabled={amountDisable}
                    value={amount}
                    onChange={(e) => onAmountChange && onAmountChange(Number(e.target.value))}
                />
            </div>

            {/* Right Side: Currency Selection */}
            <div className="w-1/2 flex flex-wrap justify-end text-right">
                <p className="text-black/40 mb-2 w-full">Currency Type</p>
                <select
                    className="rounded-lg px-1 py-1 bg-gray-100 cursor-pointer outline-none"
                    value={selectCurrency}
                    onChange={(e) => onCurrencyChange && onCurrencyChange(e.target.value)}
                    disabled={currencyDisable}
                >
                    {/* Loop through all currency options */}
                    {currencyOptions.map((currency) => (
                        <option key={currency} value={currency}>
                            {currency.toUpperCase()}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    );
}

export default InputBox;