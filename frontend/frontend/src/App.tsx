import React, { useState } from 'react';
import './App.css';
import SubmissionForm from './components/SubmissionForm';
import VerificationInterface from './components/VerificationInterface';
import BountyFunding from './components/BountyFunding';
import PayoutClaiming from './components/PayoutClaiming';
import WalletConnection from './components/WalletConnection';
import { apiClient } from './services/api';

interface TabProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabNavigation: React.FC<TabProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'submit', label: 'Submit Content' },
    { id: 'verify', label: 'Verify Submissions' },
    { id: 'fund', label: 'Fund Bounties' },
    { id: 'claim', label: 'Claim Payouts' },
  ];

  return (
    <nav className="tab-navigation">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => setActiveTab(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  );
};

function App() {
  const [activeTab, setActiveTab] = useState('submit');
  const [apiStatus, setApiStatus] = useState<string>('Checking...');

  React.useEffect(() => {
    apiClient.healthCheck()
      .then(() => setApiStatus('Connected ✅'))
      .catch(() => setApiStatus('Disconnected ❌'));
  }, []);

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'submit':
        return <SubmissionForm />;
      case 'verify':
        return <VerificationInterface />;
      case 'fund':
        return <BountyFunding />;
      case 'claim':
        return <PayoutClaiming />;
      default:
        return <SubmissionForm />;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔗 Blockchain POC Interface</h1>
        <p className="api-status">Backend API: {apiStatus}</p>
      </header>

      <main className="App-main">
        <WalletConnection />
        <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
        <div className="tab-content">
          {renderActiveTab()}
        </div>
      </main>
    </div>
  );
}

export default App;
