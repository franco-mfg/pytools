class Debug:
  """
    implementation classe for simple debug

    usage: dbg=Debug(False|True [default])

    dbg.print(data...)

    if parameter is False then nothing is printed
  """
  def __init__(self,debug=True) -> None:
    self.__DEBUG__=debug

  def print(self,*args):
    """
    usare al posto di print(...)
    stampa alcun messaggio.
    """

    if self.__DEBUG__:
      return None

    res=''
    for i in args:
      res+=f' {i}'

    print(res)
