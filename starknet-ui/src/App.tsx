import React from "react";
// import { useBlock } from "@starknet-react/core";
import Header from "./components/Header";
import './App.css';
import { callApprove } from "./connectEth";

function handleUpdates1(e: React.FormEvent<HTMLInputElement>) {
  const newValue = e.currentTarget.value;
  console.log(newValue);
  const tokenTwoValue = document.getElementById("tokenTwoValue");
  if (tokenTwoValue) {
    tokenTwoValue.innerText = (Number(newValue) / 10).toString();
  }
}

function App() {
  // useEffect()

  return (
    <main className=" flex flex-col items-center justify-center min-h-screen gap-12">
      <Header />
      <div className="flex flex-row gap-12">
      <div>
          <h2 style={{ fontFamily: 'sans-serif', fontSize: '5em',  color: 'black', margin: '4px', display: 'inline-block'}}>
            UNICHAIN🕷️
          </h2>
          <>
          <div>
            
            
            <div style={{ color: 'black', padding: "10px", border: '3.5px ', borderRadius: '30px' }}>
              
              <div className="big-card" style={{ color: 'black', backgroundColor: 'lightgrey', marginBottom: '10px' }}>
                <h2 className='tiny-label' color="black">You Pay</h2>
                
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <input 
                    className="bubble-input"
                    style={{ fontFamily: 'Comic Sans MS', marginBottom: '10px', marginRight: '400px' }} 
                    type="text" 
                    id="token-one-amount" 
                    /*value={token1Amount} */
                    onChange={(e) => {handleUpdates1(e)}}
                  />
                  <select 
                    id="tokenOne"
                    className="token-select" 
                    /*value={token1}*/ 
                    /*onChange={handleToken1Change} */
                    style={{ marginBottom: '20px' }}>
                    <option value="Choose">Choose</option>
                    <option value="0x5FbDB2315678afecb367f032d93F642f64180aa3">USD Coin (USDC)</option>
                  </select>
                </div>

              </div>
              {/* border: '3.5px solid black', */}

              <div className="big-card" style={{ color: 'black', backgroundColor: 'lightgrey' }}>
                <h3 className='tiny-label'> You Receive </h3>

                <div>
                  <div id="tokenTwoValue" className="info-box" style={{ fontFamily: 'Comic Sans MS', display: 'inline-block', marginRight: '400px'}}>
                    {/*token2Amount*/}                  
                  </div>

                  <select id="tokenTwo" className="token-select" /*value={"yes"} /*onChange={}*/>
                    <option value="Choose">Choose</option>
                    <option value="0x055d6355d99370742bf6acf65a337a3825628e9ebc4e24a7c29f9ba1c62e5a6f">Unichain on Starknet (UNX)</option>
                  </select>
                </div>
              </div>
            

              <div style={{marginTop: '5px'}}> </div>


                <p className="message">{/*message*/}</p>
            </div>
    
          </div>
          
        </> 
        {/* MAKE IT SO THAT U CANT CLICK IF NOT CONNECTED*/}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', marginBottom: '5px'}}>
          <button className="big-card" onClick={() => callApprove(localStorage.getItem("starknet") as string)}>SWAP</button>
        </div>
        </div>
      </div>
    </main>
  );
}

export default App;
