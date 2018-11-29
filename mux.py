#!/usr/bin/env python
#
#    LIP6
#    University Pierre & Marie Curie - UPMC
#    4, place Jussieu 75252 Paris Cedex 05
#    France
#
# +-----------------------------------------------------------------+
# |                                                                 |
# |                      M a s t e r   S E S I                      |
# |                  U E   T O O L S  -  T M E   3                  |
# |                                                                 |
# |  Author  . . . . . . . . . . . . . . . . . .   Sophie Belloeil  |
# |  Status  . . . . . . . . . . . . . . . . . . . . .  "./mux.py"  |
# |  Version   . . . . . . . . . . . . . . . . . . . . . . .   1.0  |
# |  Date  . . . . . . . . . . . . . . . . . . .   January 08 2010  |
# |                                                                 |
# +-----------------------------------------------------------------+


import sys
import optparse
from stratus import *


class mux ( Model ) :

  def Interface ( self ):
   # Recuperation du parametre "nbit".
    self.n   = self._param['nbit']

   # Declaration des connecteurs.
    self.i0  = SignalIn  ( "i0"  , self.n )
    self.i1  = SignalIn  ( "i1"  , self.n )
    self.cmd = SignalIn  ( "cmd" , 1      )
    self.s   = SignalOut ( "s"   , self.n )
    self.vdd = VddIn     ( "vdd" )
    self.vss = VssIn     ( "vss" )
    return

  def Netlist ( self ) :
   # Instanciation du vecteur de 'n' multiplexeurs.
    for i in range ( self.n ) :
      Inst ( "mx2_x2_%d" %self.n
           , map = { 'i0'  : self.i0[i]
                   , 'i1'  : self.i1[i]
                   , 'cmd' : self.cmd
                   , 'q'   : self.s[i]
                   , 'vdd' : self.vdd
                   , 'vss' : self.vss
                   }
           )
    return

  def Pattern ( self ) :
   # Nom du fichier de pattern.
    pat = PatWrite(self._name+'.pat',self)
   
   # Declaration de l'interface. 
    pat.declar ( self.i0 , 'X' )
    pat.declar ( self.i1 , 'X' )
    pat.declar ( self.cmd, 'B' )

    pat.declar ( self.s  , 'X' )
    
    pat.declar ( self.vdd, 'B' )
    pat.declar ( self.vss, 'B' )

   # Debut de la description des patterns.
    pat.pattern_begin ()
    
   # Affectation des valeurs.
    pat.affect_int ( self.vdd, 1 )
    pat.affect_int ( self.vss, 0 )
    
   # Triple boucle: pour toutes les valeurs de i0 & i1 on teste
   # la valeur en sortie du multiplexeur suivant la commande.
    for value_i0 in range ( self.n ) :
      for value_i1 in range ( self.n ) :
        for value_c in range ( 2 ) :
          pat.affect_int ( self.i0 , value_i0 )
          pat.affect_int ( self.i1 , value_i1 )
          pat.affect_int ( self.cmd, value_c  )
          
          if value_c == 1 : pat.affect_int ( self.s, value_i1 )
          else            : pat.affect_int ( self.s, value_i0 )
         # Ajout du pattern
          pat.addpat ()

    del pat
    return


if __name__ == '__main__':

  parser = optparse.OptionParser()
  parser.add_option( '-n', '--nbit', type='int', dest='nbit', help='The bus size' )
  (options, args) = parser.parse_args()

  buildModel( 'mux'
            , DoNetlist|DoPattern|RunSimulator
            , modelName="mux_%d"%options.nbit
            , parameters={ 'nbit':options.nbit } )

  sys.exit( 0 )

