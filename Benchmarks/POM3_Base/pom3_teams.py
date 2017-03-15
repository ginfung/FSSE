
"""
-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'

"""

from pom3_team import *
import math

class pom3_teams:
    def __init__(p3t, requirements, decisions):
        p3t.teams = []
        p3t.decisions = decisions
        
        # Build Each Team
        total_size = 0
        while (total_size < requirements.count):
            
            #specific sized teams
            p3t.teams.append(Team(decisions))
            total_size += decisions.team_size
            
        # Assign Initial Tasks to Each Team
        begin = 0
        for team in p3t.teams:
            percent = (float)(team.team_size) / (float)(total_size)
            end = (int)(begin+math.ceil(percent*len(requirements.tasks))-1)
            for k in range(begin, end):
                team.tasks.append(requirements.tasks[k])
            begin = end
        if ((end) < len(requirements.tasks)):
            for i in range(len(requirements.tasks) - (end)):
                p3t.teams[len(p3t.teams)-1].tasks.append(requirements.tasks[begin+i])
        
        # Mark Initial Visibility of Tasks for Each Team
        for team in p3t.teams:
            team.markTasksVisible()
        
        # Apply Effect of Boehm-Turner Personnel Scales to Task Costs
        scales_alpha = [0.45, 0.50, 0.55, 0.60, 0.65]
        scales_beta  = [0.40, 0.30, 0.20, 0.10, 0.00]
        scales_gamma = [0.15, 0.20, 0.25, 0.30, 0.35]
        for team in p3t.teams:
            
            numAlphas = scales_alpha[decisions.size]*team.team_size
            numBetas = scales_beta[decisions.size]*team.team_size
            numGammas = scales_gamma[decisions.size]*team.team_size
            #print numAlphas, numBetas, numGammas
            team.alpha = numAlphas
            team.beta = numBetas
            team.gamma = numGammas
            team.power = team.alpha + 1.22*team.beta + 1.6*team.gamma
            
            for task in team.tasks:
                task.val.cost += task.val.cost * ((numAlphas + 1.22*numBetas + 1.6*numGammas)/100.0)
                
                # and apply effect of criticality while we're at it
                task.val.cost = task.val.cost * (team.decisions.criticality_modifier ** team.decisions.criticality) # cost' = cost * X^criticality    
        
        #Print Out of Teams & Requirements
        """  
        for i,team in enumerate(p3t.teams): 
            print "___________________TEAM #" + str(i) + "______________________"
            for e,task in enumerate(team.tasks):
                print "> TASK #" + str(e) + ": " + str(task)
        """