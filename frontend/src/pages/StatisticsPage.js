// src/pages/StatisticsPage.js
import PapersPerYearChart from '../components/PapersPerYearChart';
import MajorsPerYearChart from '../components/MajorsPerYearChart';
import TopTeachersChart from '../components/TopTeachersChart';

function StatisticsPage() {
  return (
    <div className="App">
      <PapersPerYearChart />
      <MajorsPerYearChart />
      <TopTeachersChart />
    </div>
  );
}

export default StatisticsPage;
