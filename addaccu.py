#!/usr/bin/env python

import sys
import optparse
from stratus import *


class addaccu ( Model ) :

  def Interface ( self ):
   # Recuperation du parametre "nbit".
    self.n       = self._param['nbit']

   # Declaration des connecteurs.
    self.a       = SignalIn  ( "a"       , self.n )
    self.b       = SignalIn  ( "b"       , self.n )
    self.sel     = SignalIn  ( "sel"     , 1 )
    self.horloge = SignalIn  ( "horloge" , 1  )
    self.s       = SignalOut ( "s"       , self.n ) 
    self.vdd     = VddIn     ( "vdd" )
    self.vss     = VssIn     ( "vss" )
    return

  def Netlist ( self ) :
   # Instanciation du vecteur de 'n' multiplexeurs.
    for i in range ( self.n ) :
      Inst ( "sff1_x4_%d" %i
           , map = { 'i'  : self.d[i]
                   , 'q'  : self.q[i]
                   , 'ck' : self.horloge
                   , 'vdd' : self.vdd
                   , 'vss' : self.vss
                   }
           )
    return

  def Pattern ( self ) :
   # Nom du fichier de pattern.
    pat = PatWrite(self._name+'.pat',self)
   
   # Declaration de l'interface. 
    pat.declar ( self.d , 'X' )

    pat.declar ( self.q , 'X' )
 
    pat.declar ( self.horloge  , 'B' )
    
    pat.declar ( self.vdd, 'B' )
    pat.declar ( self.vss, 'B' )

   # Debut de la description des patterns.
    pat.pattern_begin ()
    
   # Affectation des valeurs.
    pat.affect_int ( self.vdd, 1 )
    pat.affect_int ( self.vss, 0 )
    
   # Triple boucle: pour toutes les valeurs de i0 & i1 on teste
   # la valeur en sortie du multiplexeur suivant la commande.
    for value_d in range ( self.n ) :
			for value_horloge in range ( 2 ) :
				pat.affect_int ( self.d 		 , value_d )
				pat.affect_int ( self.horloge, value_horloge  )
        
				if value_horloge == 1 : pat.affect_int ( self.q, value_d )
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

  buildModel( 'reg'
            , DoNetlist|DoPattern|RunSimulator
            , modelName="reg_%d"%options.nbit
            , parameters={ 'nbit':options.nbit } )

  sys.exit( 0 )

