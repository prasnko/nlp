Code is written in python and I have attached the corresponding automata and output on the input text provided.


q0->Initial state
q1->State entered if input is month(Word format)->L(Months)
q2->State entered if input is date(day numeral)->0<x<32
q3->State entered if input is year(year numeral)->999<x<3001
qf->Final State

(current state,input symbol)->output symbol
(q1,'of')->q2
(q2,['th','nd','rd','st','of'])->q2

L(Holidays)-Christmas,Labor,Thanksgiving,Winter,Memorial,Independence

L(Months)- Jan,Feb,.....Dec
	   January,February,...December

L(DateJoined)-> 1st,2nd,...31st



....10th August, 105 people

Above case handled using the variable 'traversalComplete'
