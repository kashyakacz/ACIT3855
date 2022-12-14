import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://acit3855-lab6.westus3.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Daily Steps</th>
							<th>Calories Burned</th>
						</tr>
						{/* <tr>
							<td># BP: {stats['num_bp_readings']}</td>
							<td># HR: {stats['num_hr_readings']}</td>
						</tr> */}
						<tr>
							<td colspan="2">Min Daily Steps: {stats['min_daily_steps']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Daily Steps: {stats['max_daily_steps']}</td>
						</tr>
						<tr>
							<td colspan="2">Min Calories Burned: {stats['min_calories_burned']}</td>
						</tr>
						<tr>
							<td colspan="2">Min Calories Burned: {stats['max_calories_burned']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
