import React from "react";
import { Link } from "react-router-dom";
import logo from "../logo.png";
import "./Navbar.css";

function Navbar() {
  return (
    <header >
      <div className="logo">
        <img src={logo} alt="Pizza logo" />
        <h1>The Pizza Society</h1>
      </div>
      <nav className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/restaurants">Restaurants</Link>
        <Link to="/pizzas">Pizzas</Link>
      </nav>
    </header>
  );
}

export default Navbar;
