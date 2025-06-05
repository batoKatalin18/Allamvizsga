// src/pages/StatisticsPage.js
import PapersPerYearChart from '../components/PapersPerYearChart';
import MajorsPerYearChart from '../components/MajorsPerYearChart';
import TopTeachersChart from '../components/TopTeachersChart';
import MostCommonKeywordsCloud from '../components/MostCommonKeywordsCloud';

function StatisticsPage() {
  return (
    <div className="App">
      <PapersPerYearChart />
      <MajorsPerYearChart />
      <TopTeachersChart />
      <MostCommonKeywordsCloud />
    </div>
  );
}

export default StatisticsPage;
