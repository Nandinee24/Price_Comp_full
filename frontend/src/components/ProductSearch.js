import React, { useState } from 'react';
import axios from 'axios';
import './ProductSearch.css';
import PriceChart from './PriceChart';
import ProductDetails from './ProductDetails';
import { HashLoader } from 'react-spinners';

function ProductSearch() {
    const [productUrl, setProductUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const searchProduct = async () => {
        setLoading(true); // Set loading to true when starting the request
        try {
            const response = await axios.get('http://localhost:8000/scrape/search/', {
                params: { product_url: productUrl }
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false); // Set loading to false after the request is complete
        }
    };

    return (
        <div className='start'>
            <div className="product-search-container">
                <h1>Product Price Comparison</h1>
                <input
                    type="text"
                    value={productUrl}
                    onChange={(e) => setProductUrl(e.target.value)}
                    placeholder="Enter product URL"
                />
                <button onClick={searchProduct}>Search</button>
                {loading ? (
                    <div className="spinner-container">
                        <HashLoader color={"#3ed6bc"} loading={loading} size={35} />
                        <p>Processing...</p>
                    </div>
                ) : result && (
                    <div className="result">
                        <h3>Product Data:</h3>
                        <p><strong>Product:</strong> {result.product_name || 'Product name not available'}</p>
                        <div className="container">
                            <PriceChart data={result} />
                            {result.image_url && <img src={result.image_url} alt="Product" />}
                        </div>
                        <div className="product-data">

                            {result.site_data && result.site_data.map((siteData, index) => (

                                <ProductDetails
                                    key={index}
                                    siteName={siteData.site_name}
                                    offers={siteData.offers}
                                    rating={siteData.rating}
                                    price={siteData.price}
                                    imageUrl={siteData.image_url}
                                />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ProductSearch;
