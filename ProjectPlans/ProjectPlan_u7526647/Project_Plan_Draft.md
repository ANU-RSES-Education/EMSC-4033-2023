**Waveform Pre-processing for Rare Seismic Phases**

**Executive Summary**
PKJKP waves are difficult to observe due to their low amplitude and high noise arriving at the same time. Additionally, they can only be observed in a small observation window, at a specific epicentral distance and only for high magnitude events. In this project, I plan to provide an interactive tool that simplifies the pre-processing of these waves and a notification system that alerts the user when a new event with favourable parameters occurred.

**Goals**
(1)	Provide a list of suitable earthquake events based on the seismic stations chosen by the user.
(2)	Conduct seismic pre-processing of the waveforms by using the parameters recommended in literature or specified by the user.
(3)	Display the waveforms in the appropriate time window.
(4)	Create additional graphics/images (e.g., a map of the analysed earthquake events) that can be used in the presentation of results.
(5)	Notify the user when a new, interesting earthquake event has occurred.

**Background and Innovation**
Already existing:
•	Obspy (python library for seismic data acquisition and pre-processing)
•	“An ObsPy library for event detection and seismic attribute calculation: preparing waveforms for automated analysis” (https://github.com/rossjturner/seismic_attributes); processing of seismic signals for NON-earthquake sources
•	Some computer programs dedicated to the processing and analysis of seismic data 
•	Computer programs to produce synthetic seismograms
•	All existing code is very specialised and most research groups just develop their own programs for their research needs
What’s new: 
•	Focus on PKJKP waves (and possibly other rare seismic waves)
•	Interactive software using obspy
•	Notifications

**Resources**
Obspy (free access) -> add extra functionality, data from servers like IRIS (free)

