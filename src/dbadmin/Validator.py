from kivy import Logger
#------------------------------------------------------------
#----------------Validator-----------------------------------
#------------------------------------------------------------

#The validate function performs validations on the data buffers
class Validator():

    def validate(self, buffer_stream, data_buffer):
        #Run validations
        if data_buffer.type == 0:
            #The buffer data type is not assigned, perform no operations
            Logger.debug('Validations: Buffer Data Type not assigned')
            data_buffer.add_error('Data Buffer Type not assigned')
        elif data_buffer.type == 1:
            Logger.debug('Product Validation Initialized')
            #Ensure the buffer is long enough
            if len(data_buffer.data) < 2:
                data_buffer.add_error('Missing Fields in data buffer')
            else:
                #Base layer validations
                if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                    data_buffer.add_error('Product ID is a required field') 
                    return True
                #Ensure the first element is an integer
                first_element = "%s" % (data_buffer.data[0])
                if first_element.isdigit() == False:
                    data_buffer.add_error('Product ID should be an integer') 
                if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                    data_buffer.add_error('Product Name is a required field') 
                    return True
                elif len('%s' % (data_buffer.data[1])) < 2:
                    data_buffer.add_error('Insufficient Product Name length') 
            
                namestring = '%s' % (data_buffer.data[1])
                if namestring[0].isupper() == False:
                    data_buffer.add_error('First Letter of Product Name should be capitalized') 
        elif data_buffer.type == 2:
            Logger.debug('Module Validation Initialized')
            #Ensure the buffer is long enough
            if len(data_buffer.data) < 3:
                data_buffer.add_error('Missing Fields in data buffer')
            else:
                #Base layer validations
                if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                    data_buffer.add_error('Module ID is a required field') 
                    return True
                if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                    data_buffer.add_error('Product ID is a required field') 
                    return True
                #Ensure the first element is an integer
                first_element = "%s" % (data_buffer.data[0])
                if first_element.isdigit() == False:
                    data_buffer.add_error('Module ID should be an integer') 
                #Ensure the second element is an integer
                second_element = "%s" % (data_buffer.data[1])
                if second_element.isdigit() == False:
                    data_buffer.add_error('Product ID should be an integer') 
                if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                    data_buffer.add_error('Module Name is a required field') 
                    return True
                elif len('%s' % (data_buffer.data[2])) < 2:
                    data_buffer.add_error('Insufficient Module Name length')
                    
                namestring = '%s' % (data_buffer.data[2])
                if namestring[0].isupper() == False:
                    data_buffer.add_error('First Letter of Module Name should be capitalized') 
        elif data_buffer.type == 3:
            Logger.debug('System Area Validation Initialized')
            #Ensure the buffer is long enough
            if len(data_buffer.data) < 3:
                data_buffer.add_error('Missing Fields in data buffer')
            else:
                if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                    data_buffer.add_error('System Area ID is a required field') 
                    return True
                if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                    data_buffer.add_error('Module ID is a required field') 
                    return True
                #Ensure the first element is an integer
                first_element = "%s" % (data_buffer.data[0])
                if first_element.isdigit() == False:
                    data_buffer.add_error('System Area ID should be an integer') 
                #Ensure the second element is an integer
                second_element = "%s" % (data_buffer.data[1])
                if second_element.isdigit() == False:
                    data_buffer.add_error('Module ID should be an integer') 
                if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                    data_buffer.add_error('System Area Name is a required field') 
                    return True
                elif len('%s' % (data_buffer.data[2])) < 2:
                    data_buffer.add_error('Insufficient System Area Name length') 
                    
                namestring = '%s' % (data_buffer.data[2])
                if namestring[0].isupper() == False:
                    data_buffer.add_error('First Letter of System Area Name should be capitalized') 
        elif data_buffer.type == 4:
            Logger.debug('Key Action Validation Initialized')
            #Ensure the buffer is long enough
            if len(data_buffer.data) < 5:
                data_buffer.add_error('Missing Fields in data buffer')
            else:
                if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                    data_buffer.add_error('Key Action ID is a required field') 
                    return True
                if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                    data_buffer.add_error('System Area ID is a required field') 
                    return True
                #Ensure the first element is an integer
                first_element = "%s" % (data_buffer.data[0])
                if first_element.isdigit() == False:
                    data_buffer.add_error('Key Action ID should be an integer') 
                #Ensure the second element is an integer
                second_element = "%s" % (data_buffer.data[1])
                if second_element.isdigit() == False:
                    data_buffer.add_error('System Area ID should be an integer') 
                if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                    data_buffer.add_error('Key Action Name is a required field') 
                    return True
                elif len('%s' % (data_buffer.data[2])) < 2:
                    data_buffer.add_error('Insufficient Key Action Name length') 
                
            namestring = '%s' % (data_buffer.data[2])
            if namestring[0].isupper() == False:
                data_buffer.add_error('First Letter of Key Action Name should be capitalized')
        elif data_buffer.type == 5:
            #Ensure the buffer is long enough
            if len(data_buffer.data) < 3:
                data_buffer.add_error('Missing Fields in data buffer')
            else:
                Logger.debug('Input Parameter Validation Initialized')
                if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                    data_buffer.add_error('Input Parameter ID is a required field') 
                    return True
                if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                    data_buffer.add_error('Key Action ID is a required field') 
                    return True
                #Ensure the first element is an integer
                first_element = "%s" % (data_buffer.data[0])
                if first_element.isdigit() == False:
                    data_buffer.add_error('Key Action ID should be an integer') 
                #Ensure the second element is an integer
                second_element = "%s" % (data_buffer.data[1])
                if second_element.isdigit() == False:
                    data_buffer.add_error('Input Parameter ID should be an integer') 
                if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                    data_buffer.add_error('Input Parameter Name is a required field') 
                    return True
                elif len('%s' % (data_buffer.data[2])) < 2:
                    data_buffer.add_error('Insufficient Input Parameter Name length') 
                
            namestring = '%s' % (data_buffer.data[2])
            if namestring[0].isupper() == False:
                data_buffer.add_error('First Letter of Input Parameter Name should be capitalized')
        elif data_buffer.type == 6:
            Logger.debug('Client Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Client ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Client Name is a required field') 
                return True
            elif len('%s' % (data_buffer.data[1])) < 2:
                data_buffer.add_error('Insufficient Client Name length') 
            
            namestring = '%s' % (data_buffer.data[1])
            if namestring[0].isupper() == False:
                data_buffer.add_error('First Letter of Client Name should be capitalized') 
        elif data_buffer.type == 7:
            Logger.debug('Project Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Project ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Client ID is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Project Name is a required field') 
                return True
            elif len('%s' % (data_buffer.data[2])) < 2:
                data_buffer.add_error('Insufficient Project Name length')
                
            namestring = '%s' % (data_buffer.data[2])
            if namestring[0].isupper() == False:
                data_buffer.add_error('First Letter of Project Name should be capitalized') 
        elif data_buffer.type == 8:
            Logger.debug('Test Script Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Test Script ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Project ID is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Test Script Name is a required field') 
                return True
            elif len('%s' % (data_buffer.data[2])) < 2:
                data_buffer.add_error('Insufficient Test Script Name length')
                
            namestring = '%s' % (data_buffer.data[2])
            if namestring[0].isupper() == False:
                data_buffer.add_error('First Letter of Test Script Name should be capitalized') 
        elif data_buffer.type == 9:
            Logger.debug('Workflow Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Workflow ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Test Script ID is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Workflow Name is a required field') 
                return True
            elif len('%s' % (data_buffer.data[2])) < 2:
                data_buffer.add_error('Insufficient Workflow Name length')
                
            namestring = '%s' % (data_buffer.data[2])
            if namestring[0].isupper() == False:
                data_buffer.add_error('First Letter of Workflow Name should be capitalized')  
        elif data_buffer.type == 10:
            Logger.debug('Workflow Action Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Workflow Action ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Workflow ID is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Key Action ID is a required field') 
        elif data_buffer.type == 11:
            Logger.debug('Workflow Next Action Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Workflow Next Action ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Workflow First Action ID is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Workflow Second Action ID is a required field') 
        elif data_buffer.type == 12:
            Logger.debug('Workflow Parameter Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Workflow Parameter ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Workflow Action ID is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Input Parameter ID is a required field') 
            if data_buffer.data[3] == '' or data_buffer.data[3] is None:
                data_buffer.add_error('Workflow Parameter Value is a required field') 
        elif data_buffer.type == 13:
            Logger.debug('Flowchart Validation Initialized')
            if data_buffer.data[0] == '' or data_buffer.data[0] is None:
                data_buffer.add_error('Next Action ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[1] is None:
                data_buffer.add_error('Key Action ID is a required field') 
            if data_buffer.data[1] == '' or data_buffer.data[2] is None:
                data_buffer.add_error('Row is a required field') 
            if data_buffer.data[2] == '' or data_buffer.data[3] is None:
                data_buffer.add_error('Column is a required field') 

        data_buffer.next_status()
        buffer_stream.task_done()