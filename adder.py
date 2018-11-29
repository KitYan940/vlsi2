#!/usr/bin/env python

import sys
import optparse
from stratus import *


class adder ( Model ) :

	def fulladder ( self, sig_a, sig_b, sig_cin, sig_s, sig_cout, sig_vdd, sig_vss ):
		self.ng 	= Signal ( "nq" 	, 1 )
		self.np_c = Signal ( "np_c" , 1 )
		self.p 		= SIgnal ( "p"		, 1 )

    Inst ( "na2_x1"
				 , map = { 'i0'  : sig_a
								 , 'i1'  : sig_b
								 , 'nq'  : self.ng
								 , 'vdd' : sig_vdd
								 , 'vss' : sig_vss
								 }
				 )

		Inst ( "xr2_x1"
				 , map = { 'i0'  : sig_a
								 , 'i1'  : sig_b
								 , 'q' 	 : self.p
								 , 'vdd' : sig_vdd
								 , 'vss' : sig_vss
								 }
				 )

		Inst ( "na2_x1"
				 , map = { 'i0'  : self.p
								 , 'i1'  : sig_cin
								 , 'nq'  : self.np_c
								 , 'vdd' : sig_vdd
								 , 'vss' : sig_vss
								 }
				 )

	 	Inst ( "na2_x1"
				 , map = { 'i0'  : self.ng
								 , 'i1'  : self.np_c
								 , 'nq'  : sig_cout
								 , 'vdd' : sig_vdd
								 , 'vss' : sig_vss
								 }
				 )	

		Inst ( "xr2_x1"±
				 , map = { 'i0'  : self.p
								 , 'i1'  : sig_cin
								 , 'q' 	 : sig_s
								 , 'vdd' : sig_vdd
								 , 'vss' : sig_vss
								 }
				 )

		return

  def Interface ( self ):
   # Recuperation du parametre "nbit".
    self.n       = self._param['nbit']

   # Declaration des connecteurs.
    self.i0     = SignalIn  ( "i0"   , self.n )
    self.i1     = SignalIn  ( "i1"   , self.n )
    self.cin    = SignalIn  ( "cin"  , 1 )
		self.cout 	= SignalOut ( "cout" , 1 )
		self.q			= SignalOut ( "q" 	 , self.n )
    self.vdd    = VddIn     ( "vdd" )
    self.vss    = VssIn     ( "vss" )
    return

  def Netlist ( self ) :
   # Instanciation du vecteur de 'n' multiplexeurs.
		self.cin_in = Signal ( "cin_in", self.n-1 )

    for i in range ( self.n ) :
			if i == 0 :
				self.fulladder ( self.i0[i], self.i1[i], self.cin, self.q[i], self.cin_in[i], self.vdd, self.vss )
      elif i == self.n-1 :
				self.fulladder ( self.i0[i], self.i1[i], self.cin_in[i-1], self.q[i], self.cout, self.vdd, self.vss )
			else :
				self.fulladder ( self.i0[i], self.i1[i], self.cin_in[i-1], self.q[i], self.cin_in[i], self.vdd, self.vss )
		return

  def Pattern ( self ) :
   # Nom du fichier de pattern.
    pat = PatWrite(self._name+'.pat',self)
   
   # Declaration de l'interface. 
    pat.declar ( self.i0   , 'X' )
    pat.declar ( self.i1   , 'X' )
		pat.declar ( self.cin  , 'B' )
 
    pat.declar ( self.cout , 'B' )
		pat.declar ( self.q 	 , 'X' )
    
    pat.declar ( self.vdd, 'B' )
    pat.declar ( self.vss, 'B' )

   # Debut de la description±
    
   # Affectation des valeurs.
    pat.affect_int ( self.vdd, 1 )
    pat.affect_int ( self.vss, 0 )
    
   # Triple boucle: pour toutes les valeurs de i0 & i1 on teste
   # la valeur en sortie du multiplexeur suivant la commande.
    for value_cin in range ( 2 ) :
			for value_i1 in range ( self.n ) :
				for value_i0 in range ( self.n ) :
					pat.affect_int ( self.cin , value_cin )
					pat.affect_int ( self.i1	, value_i1  )
					pat.affect_int ( self.i0	, value_i0  )
					
					if value_cin + value_i1 + value_i0 >= 2**self.n :
						pat.affect_int ( self.cout, 1 )
					else :
						pat.affect_int ( self.cout, 0 )
					pat.affect_int ( self.s, value_cin + value_i1 + value_i0 )
					# Ajout du pattern
					pat.addpat ()

    del pat
    return


if __name__ == '__main__':

  parser = optparse.OptionParser()
  parser.add_option( '-n', '--nbit', type='int', dest='nbit', help='The bus size' )
  (options, args) = parser.parse_args()

	if options.nbit < 2 :
		options.nbit = 2
	elif options.nbit > 64 :
		options.nbit = 64

  buildModel( 'adder'
            , DoNetlist|DoPattern|RunSimulator
            , modelName="adder_%d"%options.nbit
            , parameters={ 'nbit':options.nbit } )

  sys.exit( 0 )

