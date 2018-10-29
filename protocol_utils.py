#
#   Auxiliar file to keep all protocol utilities, including protocol macros
#

# Macros
MAX_HEADER_LEN = 16

# General function to pack data
def pack_data (data_dict):
    message = ""
    for key in data_dict:
        key_size = len(key)
        message += str(key)
        message += " " * (MAX_HEADER_LEN - key_size)
        message += str(data_dict[key])
        message += '\n'
    return message

# General function to unpack data
def unpack_data (message):
    data_dict = {}
    for line in message.split('\n'):
        line_data = [data for data in line.split(" ") if data != '']
        if (len (line_data) >= 2):
            data_dict [line_data[0]] = ''.join(line_data[1:])
    return data_dict

# Generate a request
def generate_request (data):
    try:
        cpf = str(data['cpf'])
        password = str(data['password'])
    except:
        return generate_response ({
            "status" : 7
        })
    data_dict = {}
    data_dict ['GET'] = cpf
    data_dict ['TAMANHO'] = len(password)
    data_dict ['PASSWORD'] = password
    return pack_data (data_dict)

# Generating a response
def generate_response (data):
    # Tries to get status
    try:
        status = str(data['status'])
    except:
        status = 0
    # If status 0, tries to get remaining data
    if (status == '0'):
        empty_fields = []
        # Trying CPF
        try:
            cpf = str(data['cpf'])
        except:
            return generate_response ({
                "status" : '1' + " Identificação necessária"
            })
        # Trying CURSO
        try:
            curso = str(data['curso'])
        except:
            empty_fields.append('CURSO')
        # Trying DRE
        try:
            dre = str(data['dre'])
        except:
            empty_fields.append('DRE')
        # Trying NASC
        try:
            nasc = str(data['nasc'])
        except:
            empty_fields.append('NASC')
        # Trying TAMANHO
        try:
            tamanho = str(data['tamanho'])
        except:
            empty_fields.append('TAMANHO')
        # Trying NOME
        try:
            nome = str(data['nome'])
        except:
            empty_fields.append('NOME')
        # Trying FOTO
        try:
            foto = str(data['foto'])
        except:
            empty_fields.append('FOTO')
        # Checking if any field is missing
        if (empty_fields != []):
            return pack_data ({
                "STATUS" : "6" + " Campos sem informação",
                "CAMPO" : str(empty_fields),
            })
        # Returning no error response
        else:
            return pack_data({
                "STATUS" : str(status) + " OK",
                "CURSO" : curso,
                "DRE" : dre,
                "NASC" : nasc,
                "TAMANHO" : tamanho,
                "NOME" : nome,
                "FOTO" : foto
            })
    # Returning general error response
    else:
        if str(status) == '0':
            msg = "OK"
        elif str(status) == '1':
            msg = "Identificação necessária"
        elif str(status) == '2':
            msg = "Senha incorreta"
        elif str(status) == '3':
            msg = "CPF não registrado ou incorreto"
        elif str(status) == '4':
            msg = "DRE inativo ou carteirinha já expirada"
        elif str(status) == '5':
            msg = "Foto não encontrada"
        return pack_data({
            "STATUS" : str(status) + " " + msg
        })
    pass

# Testing
if __name__ == '__main__':

    request = generate_request({"cpf" : 45049725810, "password" : 5077})
    response = generate_response({
        "status" : 0,
        "cpf" : 45049725810
    })
    print (response)