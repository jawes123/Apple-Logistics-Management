import React from "react";
import logo from "../../assets/logo.png"
import { useNavigate } from "react-router-dom";
import { HomeContainer, Logo, Options, StyledButton } from "./home.styles";

const Home = () => {
    const navigate = useNavigate();
    return(
        <HomeContainer>
            <Logo src={logo} alt="APPLE" />
            <p>Apple Logistics Management</p>
            <Options>
                <StyledButton label="View Products" onClick={() => navigate('/inventory')}/>
                <StyledButton label="Ship Items" onClick={() => navigate('/deliver')} />
                <StyledButton label="Employee Views" onClick={() => navigate('/log')}/>
            </Options>
        </HomeContainer>
    )
}

export default Home;