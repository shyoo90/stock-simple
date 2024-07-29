import { useState } from 'react';
import axios from 'axios';

interface Stock {
  item_name: string;
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [stocks, setStocks] = useState<Stock[]>([]);

  const handleSearch = async (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
    if (event.target.value.length > 0) {
      const response = await axios.get(`/api/stocks?query=${event.target.value}`);
      setStocks(response.data);
    } else {
      setStocks([]);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="relative w-full max-w-xs mx-auto">
        <input
          type="text"
          value={query}
          onChange={handleSearch}
          className="border border-gray-400 p-2 w-full"
          placeholder="Search stocks..."
        />
        {stocks.length > 0 && (
          <ul className="absolute left-0 right-0 bg-white border border-gray-400 mt-1 max-h-48 overflow-auto z-10">
            {stocks.map((stock, index) => (
              <li
                key={index}
                className="p-2 hover:bg-gray-200 cursor-pointer"
                onClick={() => setQuery(stock.item_name)}
              >
                {stock.item_name}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
