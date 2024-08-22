import React from 'react';
import './ProductSearch.css'; // Import CSS file for styling if needed

const ProductDetails = ({ siteName, offers, rating, price, imageUrl }) => { // Add imageUrl
    return (
        <div className="product-details">
            <h3>Site Name: {siteName || 'N/A'}</h3>
            <p><strong>Offers:</strong> {offers || 'No offers available'}</p>
            <p><strong>Rating:</strong> {rating || 'No ratings available'}</p>
            <p><strong>Price:</strong> {price || 'Price not available'}</p>
            {/* {imageUrl && <img src={imageUrl} alt="Product" />} Add this line */}
        </div>
    );
};

export default ProductDetails;
