import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

// Ticker data (Simulated for now, could be dynamic later)
const tickerData = [
  { pair: "USD/JPY", rate: "148.50", change: "+0.25%", up: true },
  { pair: "EUR/USD", rate: "1.0820", change: "-0.10%", up: false },
  { pair: "GBP/JPY", rate: "188.40", change: "+0.30%", up: true },
  { pair: "AUD/JPY", rate: "97.10", change: "+0.15%", up: true },
  { pair: "BTC/USD", rate: "45,200", change: "-1.50%", up: false },
  { pair: "ETH/USD", rate: "2,400", change: "-0.80%", up: false },
  { pair: "GOLD", rate: "2,030", change: "+0.05%", up: true },
]

export default (() => {
  const MarketTicker: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
    return (
      <div className={classNames(displayClass, "market-ticker-container")}>
        <div className="market-ticker-wrapper">
          <div className="market-ticker-content">
            {tickerData.map((item, index) => (
              <span key={index} className="ticker-item">
                <span className="ticker-pair">{item.pair}</span>
                <span className={item.up ? "ticker-rate up" : "ticker-rate down"}>
                  {item.rate} <span className="ticker-change">({item.change})</span>
                </span>
              </span>
            ))}
            {/* Duplicate for seamless scrolling */}
            {tickerData.map((item, index) => (
              <span key={`dup-${index}`} className="ticker-item">
                <span className="ticker-pair">{item.pair}</span>
                <span className={item.up ? "ticker-rate up" : "ticker-rate down"}>
                  {item.rate} <span className="ticker-change">({item.change})</span>
                </span>
              </span>
            ))}
          </div>
        </div>
      </div>
    )
  }

  MarketTicker.css = `
  .market-ticker-container {
    background: #0b0e14; /* Dark background */
    color: #e0e6ed;
    overflow: hidden;
    white-space: nowrap;
    padding: 8px 0;
    border-bottom: 1px solid #3498db;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    position: relative;
    z-index: 1001; /* Above header */
    width: 100%;
    max-width: 100vw;
    box-sizing: border-box;
  }
  
  .market-ticker-wrapper {
    display: inline-block;
    padding-left: 100%; /* Start off-screen */
    animation: ticker 30s linear infinite;
  }
  
  .market-ticker-content {
    display: inline-block;
  }
  
  .market-ticker-wrapper:hover {
    animation-play-state: paused;
  }
  
  @keyframes ticker {
    0% {
      transform: translate3d(0, 0, 0);
    }
    100% {
      transform: translate3d(-100%, 0, 0);
    }
  }
  
  .ticker-item {
    display: inline-block;
    padding: 0 1.5rem;
    border-right: 1px solid #393639;
  }
  
  .ticker-pair {
    font-weight: bold;
    margin-right: 0.5rem;
    color: #a4b1cd;
  }
  
  .ticker-rate.up {
    color: #2ecc71;
  }
  
  .ticker-rate.down {
    color: #e74c3c;
  }
  
  .ticker-change {
    font-size: 0.75rem;
    opacity: 0.8;
    margin-left: 0.2rem;
  }
  `

  return MarketTicker
}) satisfies QuartzComponentConstructor
