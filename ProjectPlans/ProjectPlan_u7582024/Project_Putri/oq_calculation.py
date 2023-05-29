"""
The oq_calculation.py is a program aimed to performs OpenQuake calculations 
required for ground motion modeling and probability of damage distribution.

Inputs of this program are XML-based data and configuration file that is generated
by `job_xml_generator.py`. The calculation that run in this program is based on 
calculation mode defined in configuration file. This program will generate gmf_data.csv, 
avg_gmf.gmf, damages-rlzs.csv, aggrisk.csv, and risk_by_event.csv.
"""

# Import all modules and libraries
import os
from openquake.engine import engine
from openquake.calculators.export import hazard
from openquake.commonlib import logs
from openquake.calculators.base import calculators
from openquake.calculators.extract import extract
from openquake.calculators.export import risk

def main():
    # Run oq engine for the first time to make sure DB server is initialized
    os.system("oq engine")

    # Path is path for location where the "job.ini" is saved. 
    # job.ini should be saved in the same folder with all input file for the calculation
    path = os.path.join(os.getcwd(),"data", "job" + ".ini")

    # Calculation based on calculation mode defined in the job.ini
    with logs.init('job', path) as log:
        calc = calculators(log.get_oqparam(), log.calc_id)
        calc.run()  # run the calculator

    # Export output file and store it in directory defined in job.ini
    hazard.export_gmf_data_csv(("gmf_data","csv"),dstore=calc.datastore)
    hazard.export_avg_gmf_csv(("avg_gmf","csv"),dstore=calc.datastore)
    risk.export_damages_csv(("damages-rlzs","csv"),dstore=calc.datastore) 
    risk.export_aggrisk(("aggrisk","csv"),dstore=calc.datastore)
    risk.export_event_loss_table(("risk_by_event","csv"),dstore=calc.datastore)

if __name__=='__main__':
    main()