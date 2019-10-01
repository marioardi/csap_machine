import time
import datetime
import openerp
from odoo import SUPERUSER_ID
from odoo import pooler, tools
from odoo.osv import osv, fields
from odooo.tools.translate import _

import sys
import zklib
from zklib import zkconst
from zklib import zklib

class fingerprint_machine(osv.osv):
    _name = 'fingerprint.machine'        
    
    def get_machine_info(self, cr, uid, ids, context=None):
        
        for record in self.browse(cr, uid, ids, context=context):
            ip_address = record.ip_address
            device_port = record.device_port
            
        zk = zklib.ZKLib(ip_address, device_port)
        ret = zk.connect()
        
        total_user = 0
        total_log = 0
        
        data_user = zk.getUser()
        if data_user:
            for x in data_user:
                total_user += 1
         
        attendance = zk.getAttendance()
        if attendance:
            for x in attendance:
                total_log += 1
               
        self.write(cr, uid, ids, {'software_version': zk.version(),
                                  'os_version': zk.osversion(),
                                  'device_platform': zk.platform(),
                                  'fm_platform': zk.fmVersion(),
                                  'device_name': zk.deviceName(),
                                  'serial_number': zk.serialNumber(),
                                  'device_time': zk.getTime(),
                                  'total_user': total_user,
                                  'total_log': total_log,
                                  })  
        zk.disconnect()
    
        return True
    
    def clear_machine_log(self, cr, uid, ids, context=None):    
        for record in self.browse(cr, uid, ids, context=context):
            ip_address = record.ip_address
            device_port = record.device_port
            
        zk = zklib.ZKLib(ip_address, device_port)
        ret = zk.connect()
        zk.clearAttendance()
        zk.disconnect()
        
        return True
    
    def get_fingerprint_user(self, cr, uid, ids, context=None):    
        
        employee_obj = self.pool.get('hr.employee')   
        
        for record in self.browse(cr, uid, ids, context=context):
            ip_address = record.ip_address
            device_port = record.device_port
            
        zk = zklib.ZKLib(ip_address, device_port)
        ret = zk.connect()
        
        data_employee = {}
        
        data_user = zk.getUser()
        print data_user
        
        if data_user:
            for x in data_user:
                data_employee['nik'] = data_user[x][0]
                data_employee['name'] = data_user[x][1]
                
                #check user exist               
                exist_user = self.pool.get('hr.employee').search(cr, uid, [('nik','=',data_user[x][0])])
                if not exist_user:     
                    employee_obj.create(cr, uid, data_employee)
                
        zk.disconnect()
        return True        
        
    def get_attendance_log(self, cr, uid, ids, context=None):    
        
        attendance_log_obj = self.pool.get('original.attendance.log')   
        employee_obj = self.pool.get('hr.employee')   
        
        for record in self.browse(cr, uid, ids, context=context):
            ip_address = record.ip_address
            device_port = record.device_port
            
        zk = zklib.ZKLib(ip_address, device_port)
        ret = zk.connect()
        
        data_log = {}
        
        attendance = zk.getAttendance()
        if attendance:
            for log in attendance:
                
                    temp_string_time = unicode(log[2].time())
                    attendance_log_ids = attendance_log_obj.search(cr, uid, [('fingerprint_id','=',log[0]),('date','=',log[2].date()),('time','=',temp_string_time)])
                    
                    #if fingerprint log is not exist, download and create new record
                    if not attendance_log_ids:
                        data_log['fingerprint_id'] = log[0]
                        data_log['date'] = log[2].date()
                        data_log['time'] = log[2].time()
                        data_log['status'] = log[1]
                        data_log['name'] = log[0]
                        
                        employee_ids = employee_obj.search(cr, uid, [('nik','=',log[0])])
                        
                        if employee_ids:
                            data_log['name'] = employee_obj.search(cr, uid, [('nik','=',log[0])])[0]
                            attendance_log_obj.create(cr, uid, data_log)
                
        zk.disconnect()
        return True
    
    _columns = {
        'name': fields.char('Device Name'),
        'ip_address': fields.char('IP Address'),
        'device_port': fields.integer('Device Port'),
        'software_version': fields.char('Software Version', readonly=True),
        'os_version': fields.char('OS Version', readonly=True),
        'device_platform': fields.char('Device Platform', readonly=True),      
        'fm_platform': fields.char('Firmware Platform', readonly=True),    
        'serial_number': fields.char('Serial Number', readonly=True),    
        'device_time': fields.char('Device Time', readonly=True),     
        'total_user': fields.char('Total User', readonly=True),    
        'total_log': fields.integer('Total Log', readonly=True),   
        'image': fields.binary('Image'),    
        'filename_image': fields.char('Filename'),    
    }  
    
    
fingerprint_machine()


class original_attendance_log(osv.osv):
    _name = 'original.attendance.log'        
    
    _columns = {
        'name': fields.many2one('hr.employee', 'Employee Name'),  
        'fingerprint_id': fields.char('Fingerprint ID'), 
        'date': fields.date('Date'),
        'time': fields.char('Time'),
        'status': fields.char('Status'),   
    }  
    
    
original_attendance_log()
