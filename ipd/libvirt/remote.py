"""
Automatically generated Libvirt protocol specification.

Do not modify this file manually, as the changes will be overwritten
the next time that the generation script is run!

  Generated on:  2014-01-17T11:55:24.499890
  Command line:  gen-libvirt-protocol ../../temp/libvirt/src/remote/remote_protocol.x ipd/libvirt/remote.py

"""

from ipd.libvirt.procedures import ProcedureBase
from ipd.libvirt.types import char, short, int, hyper
from ipd.libvirt.types import uchar, ushort, uint, uhyper
from ipd.libvirt.types import fstring, string, fopaque, opaque
from ipd.libvirt.types import farray, array, optional
from ipd.libvirt.types import not_implemented, compound, enum


PROGRAM = 0x20008086
PROTOCOL_VERSION = 0x1

nonnull_domain = compound('nonnull_domain', [
    ('name', string),
    ('uuid', fopaque(16)),
    ('id', int),
])

nonnull_network = compound('nonnull_network', [
    ('name', string),
    ('uuid', fopaque(16)),
])

nonnull_nwfilter = compound('nonnull_nwfilter', [
    ('name', string),
    ('uuid', fopaque(16)),
])

nonnull_interface = compound('nonnull_interface', [
    ('name', string),
    ('mac', string),
])

nonnull_storage_pool = compound('nonnull_storage_pool', [
    ('name', string),
    ('uuid', fopaque(16)),
])

nonnull_storage_vol = compound('nonnull_storage_vol', [
    ('pool', string),
    ('name', string),
    ('key', string),
])

nonnull_node_device = compound('nonnull_node_device', [
    ('name', string),
])

nonnull_secret = compound('nonnull_secret', [
    ('uuid', fopaque(16)),
    ('usageType', int),
    ('usageID', string),
])

nonnull_domain_snapshot = compound('nonnull_domain_snapshot', [
    ('name', string),
    ('dom', nonnull_domain),
])

error = compound('error', [
    ('code', int),
    ('domain', int),
    ('message', optional(string)),
    ('level', int),
    ('dom', optional(nonnull_domain)),
    ('str1', optional(string)),
    ('str2', optional(string)),
    ('str3', optional(string)),
    ('int1', int),
    ('int2', int),
    ('net', optional(nonnull_network)),
])

auth_type = enum('auth_type', [
    ('REMOTE_AUTH_NONE', 0),
    ('REMOTE_AUTH_SASL', 1),
    ('REMOTE_AUTH_POLKIT', 2),
])

vcpu_info = compound('vcpu_info', [
    ('number', uint),
    ('state', int),
    ('cpu_time', uhyper),
    ('cpu', int),
])

typed_param = compound('typed_param', [
    ('field', string),
    ('value', not_implemented),
])

node_get_cpu_stats = compound('node_get_cpu_stats', [
    ('field', string),
    ('value', uhyper),
])

node_get_memory_stats = compound('node_get_memory_stats', [
    ('field', string),
    ('value', uhyper),
])

domain_disk_error = compound('domain_disk_error', [
    ('disk', string),
    ('error', int),
])

connect_open_args = compound('connect_open_args', [
    ('name', optional(string)),
    ('flags', uint),
])

connect_supports_feature_args = compound('connect_supports_feature_args', [
    ('feature', int),
])

connect_supports_feature_ret = compound('connect_supports_feature_ret', [
    ('supported', int),
])

connect_get_type_ret = compound('connect_get_type_ret', [
    ('type', string),
])

connect_get_version_ret = compound('connect_get_version_ret', [
    ('hv_ver', uhyper),
])

connect_get_lib_version_ret = compound('connect_get_lib_version_ret', [
    ('lib_ver', uhyper),
])

connect_get_hostname_ret = compound('connect_get_hostname_ret', [
    ('hostname', string),
])

connect_get_sysinfo_args = compound('connect_get_sysinfo_args', [
    ('flags', uint),
])

connect_get_sysinfo_ret = compound('connect_get_sysinfo_ret', [
    ('sysinfo', string),
])

connect_get_uri_ret = compound('connect_get_uri_ret', [
    ('uri', string),
])

connect_get_max_vcpus_args = compound('connect_get_max_vcpus_args', [
    ('type', optional(string)),
])

connect_get_max_vcpus_ret = compound('connect_get_max_vcpus_ret', [
    ('max_vcpus', int),
])

node_get_info_ret = compound('node_get_info_ret', [
    ('model', farray(char, 32)),
    ('memory', uhyper),
    ('cpus', int),
    ('mhz', int),
    ('nodes', int),
    ('sockets', int),
    ('cores', int),
    ('threads', int),
])

connect_get_capabilities_ret = compound('connect_get_capabilities_ret', [
    ('capabilities', string),
])

node_get_cpu_stats_args = compound('node_get_cpu_stats_args', [
    ('cpuNum', int),
    ('nparams', int),
    ('flags', uint),
])

node_get_cpu_stats_ret = compound('node_get_cpu_stats_ret', [
    ('params', array(node_get_cpu_stats, 16)),
    ('nparams', int),
])

node_get_memory_stats_args = compound('node_get_memory_stats_args', [
    ('nparams', int),
    ('cellNum', int),
    ('flags', uint),
])

node_get_memory_stats_ret = compound('node_get_memory_stats_ret', [
    ('params', array(node_get_memory_stats, 16)),
    ('nparams', int),
])

node_get_cells_free_memory_args = compound('node_get_cells_free_memory_args', [
    ('startCell', int),
    ('maxcells', int),
])

node_get_cells_free_memory_ret = compound('node_get_cells_free_memory_ret', [
    ('cells', array(uhyper, 1024)),
])

node_get_free_memory_ret = compound('node_get_free_memory_ret', [
    ('freeMem', uhyper),
])

domain_get_scheduler_type_args = compound('domain_get_scheduler_type_args', [
    ('dom', nonnull_domain),
])

domain_get_scheduler_type_ret = compound('domain_get_scheduler_type_ret', [
    ('type', string),
    ('nparams', int),
])

domain_get_scheduler_parameters_args = compound('domain_get_scheduler_parameters_args', [
    ('dom', nonnull_domain),
    ('nparams', int),
])

domain_get_scheduler_parameters_ret = compound('domain_get_scheduler_parameters_ret', [
    ('params', array(typed_param, 16)),
])

domain_get_scheduler_parameters_flags_args = compound('domain_get_scheduler_parameters_flags_args', [
    ('dom', nonnull_domain),
    ('nparams', int),
    ('flags', uint),
])

domain_get_scheduler_parameters_flags_ret = compound('domain_get_scheduler_parameters_flags_ret', [
    ('params', array(typed_param, 16)),
])

domain_set_scheduler_parameters_args = compound('domain_set_scheduler_parameters_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 16)),
])

domain_set_scheduler_parameters_flags_args = compound('domain_set_scheduler_parameters_flags_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 16)),
    ('flags', uint),
])

domain_set_blkio_parameters_args = compound('domain_set_blkio_parameters_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 16)),
    ('flags', uint),
])

domain_get_blkio_parameters_args = compound('domain_get_blkio_parameters_args', [
    ('dom', nonnull_domain),
    ('nparams', int),
    ('flags', uint),
])

domain_get_blkio_parameters_ret = compound('domain_get_blkio_parameters_ret', [
    ('params', array(typed_param, 16)),
    ('nparams', int),
])

domain_set_memory_parameters_args = compound('domain_set_memory_parameters_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 16)),
    ('flags', uint),
])

domain_get_memory_parameters_args = compound('domain_get_memory_parameters_args', [
    ('dom', nonnull_domain),
    ('nparams', int),
    ('flags', uint),
])

domain_get_memory_parameters_ret = compound('domain_get_memory_parameters_ret', [
    ('params', array(typed_param, 16)),
    ('nparams', int),
])

domain_block_resize_args = compound('domain_block_resize_args', [
    ('dom', nonnull_domain),
    ('disk', string),
    ('size', uhyper),
    ('flags', uint),
])

domain_set_numa_parameters_args = compound('domain_set_numa_parameters_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 16)),
    ('flags', uint),
])

domain_get_numa_parameters_args = compound('domain_get_numa_parameters_args', [
    ('dom', nonnull_domain),
    ('nparams', int),
    ('flags', uint),
])

domain_get_numa_parameters_ret = compound('domain_get_numa_parameters_ret', [
    ('params', array(typed_param, 16)),
    ('nparams', int),
])

domain_block_stats_args = compound('domain_block_stats_args', [
    ('dom', nonnull_domain),
    ('path', string),
])

domain_block_stats_ret = compound('domain_block_stats_ret', [
    ('rd_req', hyper),
    ('rd_bytes', hyper),
    ('wr_req', hyper),
    ('wr_bytes', hyper),
    ('errs', hyper),
])

domain_block_stats_flags_args = compound('domain_block_stats_flags_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('nparams', int),
    ('flags', uint),
])

domain_block_stats_flags_ret = compound('domain_block_stats_flags_ret', [
    ('params', array(typed_param, 16)),
    ('nparams', int),
])

domain_interface_stats_args = compound('domain_interface_stats_args', [
    ('dom', nonnull_domain),
    ('path', string),
])

domain_interface_stats_ret = compound('domain_interface_stats_ret', [
    ('rx_bytes', hyper),
    ('rx_packets', hyper),
    ('rx_errs', hyper),
    ('rx_drop', hyper),
    ('tx_bytes', hyper),
    ('tx_packets', hyper),
    ('tx_errs', hyper),
    ('tx_drop', hyper),
])

domain_set_interface_parameters_args = compound('domain_set_interface_parameters_args', [
    ('dom', nonnull_domain),
    ('device', string),
    ('params', array(typed_param, 16)),
    ('flags', uint),
])

domain_get_interface_parameters_args = compound('domain_get_interface_parameters_args', [
    ('dom', nonnull_domain),
    ('device', string),
    ('nparams', int),
    ('flags', uint),
])

domain_get_interface_parameters_ret = compound('domain_get_interface_parameters_ret', [
    ('params', array(typed_param, 16)),
    ('nparams', int),
])

domain_memory_stats_args = compound('domain_memory_stats_args', [
    ('dom', nonnull_domain),
    ('maxStats', uint),
    ('flags', uint),
])

domain_memory_stat = compound('domain_memory_stat', [
    ('tag', int),
    ('val', uhyper),
])

domain_memory_stats_ret = compound('domain_memory_stats_ret', [
    ('stats', array(domain_memory_stat, 1024)),
])

domain_block_peek_args = compound('domain_block_peek_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('offset', uhyper),
    ('size', uint),
    ('flags', uint),
])

domain_block_peek_ret = compound('domain_block_peek_ret', [
    ('buffer', opaque),
])

domain_memory_peek_args = compound('domain_memory_peek_args', [
    ('dom', nonnull_domain),
    ('offset', uhyper),
    ('size', uint),
    ('flags', uint),
])

domain_memory_peek_ret = compound('domain_memory_peek_ret', [
    ('buffer', opaque),
])

domain_get_block_info_args = compound('domain_get_block_info_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('flags', uint),
])

domain_get_block_info_ret = compound('domain_get_block_info_ret', [
    ('allocation', uhyper),
    ('capacity', uhyper),
    ('physical', uhyper),
])

connect_list_domains_args = compound('connect_list_domains_args', [
    ('maxids', int),
])

connect_list_domains_ret = compound('connect_list_domains_ret', [
    ('ids', array(int, 16384)),
])

connect_num_of_domains_ret = compound('connect_num_of_domains_ret', [
    ('num', int),
])

domain_create_xml_args = compound('domain_create_xml_args', [
    ('xml_desc', string),
    ('flags', uint),
])

domain_create_xml_ret = compound('domain_create_xml_ret', [
    ('dom', nonnull_domain),
])

domain_create_xml_with_files_args = compound('domain_create_xml_with_files_args', [
    ('xml_desc', string),
    ('flags', uint),
])

domain_create_xml_with_files_ret = compound('domain_create_xml_with_files_ret', [
    ('dom', nonnull_domain),
])

domain_lookup_by_id_args = compound('domain_lookup_by_id_args', [
    ('id', int),
])

domain_lookup_by_id_ret = compound('domain_lookup_by_id_ret', [
    ('dom', nonnull_domain),
])

domain_lookup_by_uuid_args = compound('domain_lookup_by_uuid_args', [
    ('uuid', fopaque(16)),
])

domain_lookup_by_uuid_ret = compound('domain_lookup_by_uuid_ret', [
    ('dom', nonnull_domain),
])

domain_lookup_by_name_args = compound('domain_lookup_by_name_args', [
    ('name', string),
])

domain_lookup_by_name_ret = compound('domain_lookup_by_name_ret', [
    ('dom', nonnull_domain),
])

domain_suspend_args = compound('domain_suspend_args', [
    ('dom', nonnull_domain),
])

domain_resume_args = compound('domain_resume_args', [
    ('dom', nonnull_domain),
])

domain_pm_suspend_for_duration_args = compound('domain_pm_suspend_for_duration_args', [
    ('dom', nonnull_domain),
    ('target', uint),
    ('duration', uhyper),
    ('flags', uint),
])

domain_pm_wakeup_args = compound('domain_pm_wakeup_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_shutdown_args = compound('domain_shutdown_args', [
    ('dom', nonnull_domain),
])

domain_reboot_args = compound('domain_reboot_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_reset_args = compound('domain_reset_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_destroy_args = compound('domain_destroy_args', [
    ('dom', nonnull_domain),
])

domain_destroy_flags_args = compound('domain_destroy_flags_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_os_type_args = compound('domain_get_os_type_args', [
    ('dom', nonnull_domain),
])

domain_get_os_type_ret = compound('domain_get_os_type_ret', [
    ('type', string),
])

domain_get_max_memory_args = compound('domain_get_max_memory_args', [
    ('dom', nonnull_domain),
])

domain_get_max_memory_ret = compound('domain_get_max_memory_ret', [
    ('memory', uhyper),
])

domain_set_max_memory_args = compound('domain_set_max_memory_args', [
    ('dom', nonnull_domain),
    ('memory', uhyper),
])

domain_set_memory_args = compound('domain_set_memory_args', [
    ('dom', nonnull_domain),
    ('memory', uhyper),
])

domain_set_memory_flags_args = compound('domain_set_memory_flags_args', [
    ('dom', nonnull_domain),
    ('memory', uhyper),
    ('flags', uint),
])

domain_set_memory_stats_period_args = compound('domain_set_memory_stats_period_args', [
    ('dom', nonnull_domain),
    ('period', int),
    ('flags', uint),
])

domain_get_info_args = compound('domain_get_info_args', [
    ('dom', nonnull_domain),
])

domain_get_info_ret = compound('domain_get_info_ret', [
    ('state', uchar),
    ('maxMem', uhyper),
    ('memory', uhyper),
    ('nrVirtCpu', ushort),
    ('cpuTime', uhyper),
])

domain_save_args = compound('domain_save_args', [
    ('dom', nonnull_domain),
    ('to', string),
])

domain_save_flags_args = compound('domain_save_flags_args', [
    ('dom', nonnull_domain),
    ('to', string),
    ('dxml', optional(string)),
    ('flags', uint),
])

domain_restore_args = compound('domain_restore_args', [
    ('from_', string),
])

domain_restore_flags_args = compound('domain_restore_flags_args', [
    ('from_', string),
    ('dxml', optional(string)),
    ('flags', uint),
])

domain_save_image_get_xml_desc_args = compound('domain_save_image_get_xml_desc_args', [
    ('file', string),
    ('flags', uint),
])

domain_save_image_get_xml_desc_ret = compound('domain_save_image_get_xml_desc_ret', [
    ('xml', string),
])

domain_save_image_define_xml_args = compound('domain_save_image_define_xml_args', [
    ('file', string),
    ('dxml', string),
    ('flags', uint),
])

domain_core_dump_args = compound('domain_core_dump_args', [
    ('dom', nonnull_domain),
    ('to', string),
    ('flags', uint),
])

domain_screenshot_args = compound('domain_screenshot_args', [
    ('dom', nonnull_domain),
    ('screen', uint),
    ('flags', uint),
])

domain_screenshot_ret = compound('domain_screenshot_ret', [
    ('mime', optional(string)),
])

domain_get_xml_desc_args = compound('domain_get_xml_desc_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_xml_desc_ret = compound('domain_get_xml_desc_ret', [
    ('xml', string),
])

domain_migrate_prepare_args = compound('domain_migrate_prepare_args', [
    ('uri_in', optional(string)),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
])

domain_migrate_prepare_ret = compound('domain_migrate_prepare_ret', [
    ('cookie', opaque),
    ('uri_out', optional(string)),
])

domain_migrate_perform_args = compound('domain_migrate_perform_args', [
    ('dom', nonnull_domain),
    ('cookie', opaque),
    ('uri', string),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
])

domain_migrate_finish_args = compound('domain_migrate_finish_args', [
    ('dname', string),
    ('cookie', opaque),
    ('uri', string),
    ('flags', uhyper),
])

domain_migrate_finish_ret = compound('domain_migrate_finish_ret', [
    ('ddom', nonnull_domain),
])

domain_migrate_prepare2_args = compound('domain_migrate_prepare2_args', [
    ('uri_in', optional(string)),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
    ('dom_xml', string),
])

domain_migrate_prepare2_ret = compound('domain_migrate_prepare2_ret', [
    ('cookie', opaque),
    ('uri_out', optional(string)),
])

domain_migrate_finish2_args = compound('domain_migrate_finish2_args', [
    ('dname', string),
    ('cookie', opaque),
    ('uri', string),
    ('flags', uhyper),
    ('retcode', int),
])

domain_migrate_finish2_ret = compound('domain_migrate_finish2_ret', [
    ('ddom', nonnull_domain),
])

connect_list_defined_domains_args = compound('connect_list_defined_domains_args', [
    ('maxnames', int),
])

connect_list_defined_domains_ret = compound('connect_list_defined_domains_ret', [
    ('names', array(string, 16384)),
])

connect_num_of_defined_domains_ret = compound('connect_num_of_defined_domains_ret', [
    ('num', int),
])

domain_create_args = compound('domain_create_args', [
    ('dom', nonnull_domain),
])

domain_create_with_flags_args = compound('domain_create_with_flags_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_create_with_flags_ret = compound('domain_create_with_flags_ret', [
    ('dom', nonnull_domain),
])

domain_create_with_files_args = compound('domain_create_with_files_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_create_with_files_ret = compound('domain_create_with_files_ret', [
    ('dom', nonnull_domain),
])

domain_define_xml_args = compound('domain_define_xml_args', [
    ('xml', string),
])

domain_define_xml_ret = compound('domain_define_xml_ret', [
    ('dom', nonnull_domain),
])

domain_undefine_args = compound('domain_undefine_args', [
    ('dom', nonnull_domain),
])

domain_undefine_flags_args = compound('domain_undefine_flags_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_inject_nmi_args = compound('domain_inject_nmi_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_send_key_args = compound('domain_send_key_args', [
    ('dom', nonnull_domain),
    ('codeset', uint),
    ('holdtime', uint),
    ('keycodes', array(uint, 16)),
    ('flags', uint),
])

domain_send_process_signal_args = compound('domain_send_process_signal_args', [
    ('dom', nonnull_domain),
    ('pid_value', hyper),
    ('signum', uint),
    ('flags', uint),
])

domain_set_vcpus_args = compound('domain_set_vcpus_args', [
    ('dom', nonnull_domain),
    ('nvcpus', uint),
])

domain_set_vcpus_flags_args = compound('domain_set_vcpus_flags_args', [
    ('dom', nonnull_domain),
    ('nvcpus', uint),
    ('flags', uint),
])

domain_get_vcpus_flags_args = compound('domain_get_vcpus_flags_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_vcpus_flags_ret = compound('domain_get_vcpus_flags_ret', [
    ('num', int),
])

domain_pin_vcpu_args = compound('domain_pin_vcpu_args', [
    ('dom', nonnull_domain),
    ('vcpu', uint),
    ('cpumap', opaque),
])

domain_pin_vcpu_flags_args = compound('domain_pin_vcpu_flags_args', [
    ('dom', nonnull_domain),
    ('vcpu', uint),
    ('cpumap', opaque),
    ('flags', uint),
])

domain_get_vcpu_pin_info_args = compound('domain_get_vcpu_pin_info_args', [
    ('dom', nonnull_domain),
    ('ncpumaps', int),
    ('maplen', int),
    ('flags', uint),
])

domain_get_vcpu_pin_info_ret = compound('domain_get_vcpu_pin_info_ret', [
    ('cpumaps', opaque),
    ('num', int),
])

domain_pin_emulator_args = compound('domain_pin_emulator_args', [
    ('dom', nonnull_domain),
    ('cpumap', opaque),
    ('flags', uint),
])

domain_get_emulator_pin_info_args = compound('domain_get_emulator_pin_info_args', [
    ('dom', nonnull_domain),
    ('maplen', int),
    ('flags', uint),
])

domain_get_emulator_pin_info_ret = compound('domain_get_emulator_pin_info_ret', [
    ('cpumaps', opaque),
    ('ret', int),
])

domain_get_vcpus_args = compound('domain_get_vcpus_args', [
    ('dom', nonnull_domain),
    ('maxinfo', int),
    ('maplen', int),
])

domain_get_vcpus_ret = compound('domain_get_vcpus_ret', [
    ('info', array(vcpu_info, 16384)),
    ('cpumaps', opaque),
])

domain_get_max_vcpus_args = compound('domain_get_max_vcpus_args', [
    ('dom', nonnull_domain),
])

domain_get_max_vcpus_ret = compound('domain_get_max_vcpus_ret', [
    ('num', int),
])

domain_get_security_label_args = compound('domain_get_security_label_args', [
    ('dom', nonnull_domain),
])

domain_get_security_label_ret = compound('domain_get_security_label_ret', [
    ('label', array(char, 4097)),
    ('enforcing', int),
])

domain_get_security_label_list_args = compound('domain_get_security_label_list_args', [
    ('dom', nonnull_domain),
])

domain_get_security_label_list_ret = compound('domain_get_security_label_list_ret', [
    ('labels', array(domain_get_security_label_ret, 64)),
    ('ret', int),
])

node_get_security_model_ret = compound('node_get_security_model_ret', [
    ('model', array(char, 257)),
    ('doi', array(char, 257)),
])

domain_attach_device_args = compound('domain_attach_device_args', [
    ('dom', nonnull_domain),
    ('xml', string),
])

domain_attach_device_flags_args = compound('domain_attach_device_flags_args', [
    ('dom', nonnull_domain),
    ('xml', string),
    ('flags', uint),
])

domain_detach_device_args = compound('domain_detach_device_args', [
    ('dom', nonnull_domain),
    ('xml', string),
])

domain_detach_device_flags_args = compound('domain_detach_device_flags_args', [
    ('dom', nonnull_domain),
    ('xml', string),
    ('flags', uint),
])

domain_update_device_flags_args = compound('domain_update_device_flags_args', [
    ('dom', nonnull_domain),
    ('xml', string),
    ('flags', uint),
])

domain_get_autostart_args = compound('domain_get_autostart_args', [
    ('dom', nonnull_domain),
])

domain_get_autostart_ret = compound('domain_get_autostart_ret', [
    ('autostart', int),
])

domain_set_autostart_args = compound('domain_set_autostart_args', [
    ('dom', nonnull_domain),
    ('autostart', int),
])

domain_set_metadata_args = compound('domain_set_metadata_args', [
    ('dom', nonnull_domain),
    ('type', int),
    ('metadata', optional(string)),
    ('key', optional(string)),
    ('uri', optional(string)),
    ('flags', uint),
])

domain_get_metadata_args = compound('domain_get_metadata_args', [
    ('dom', nonnull_domain),
    ('type', int),
    ('uri', optional(string)),
    ('flags', uint),
])

domain_get_metadata_ret = compound('domain_get_metadata_ret', [
    ('metadata', string),
])

domain_block_job_abort_args = compound('domain_block_job_abort_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('flags', uint),
])

domain_get_block_job_info_args = compound('domain_get_block_job_info_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('flags', uint),
])

domain_get_block_job_info_ret = compound('domain_get_block_job_info_ret', [
    ('found', int),
    ('type', int),
    ('bandwidth', uhyper),
    ('cur', uhyper),
    ('end', uhyper),
])

domain_block_job_set_speed_args = compound('domain_block_job_set_speed_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('bandwidth', uhyper),
    ('flags', uint),
])

domain_block_pull_args = compound('domain_block_pull_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('bandwidth', uhyper),
    ('flags', uint),
])

domain_block_rebase_args = compound('domain_block_rebase_args', [
    ('dom', nonnull_domain),
    ('path', string),
    ('base', optional(string)),
    ('bandwidth', uhyper),
    ('flags', uint),
])

domain_block_commit_args = compound('domain_block_commit_args', [
    ('dom', nonnull_domain),
    ('disk', string),
    ('base', optional(string)),
    ('top', optional(string)),
    ('bandwidth', uhyper),
    ('flags', uint),
])

domain_set_block_io_tune_args = compound('domain_set_block_io_tune_args', [
    ('dom', nonnull_domain),
    ('disk', string),
    ('params', array(typed_param, 16)),
    ('flags', uint),
])

domain_get_block_io_tune_args = compound('domain_get_block_io_tune_args', [
    ('dom', nonnull_domain),
    ('disk', optional(string)),
    ('nparams', int),
    ('flags', uint),
])

domain_get_block_io_tune_ret = compound('domain_get_block_io_tune_ret', [
    ('params', array(typed_param, 16)),
    ('nparams', int),
])

domain_get_cpu_stats_args = compound('domain_get_cpu_stats_args', [
    ('dom', nonnull_domain),
    ('nparams', uint),
    ('start_cpu', int),
    ('ncpus', uint),
    ('flags', uint),
])

domain_get_cpu_stats_ret = compound('domain_get_cpu_stats_ret', [
    ('params', array(typed_param, 2048)),
    ('nparams', int),
])

domain_get_hostname_args = compound('domain_get_hostname_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_hostname_ret = compound('domain_get_hostname_ret', [
    ('hostname', string),
])

connect_num_of_networks_ret = compound('connect_num_of_networks_ret', [
    ('num', int),
])

connect_list_networks_args = compound('connect_list_networks_args', [
    ('maxnames', int),
])

connect_list_networks_ret = compound('connect_list_networks_ret', [
    ('names', array(string, 16384)),
])

connect_num_of_defined_networks_ret = compound('connect_num_of_defined_networks_ret', [
    ('num', int),
])

connect_list_defined_networks_args = compound('connect_list_defined_networks_args', [
    ('maxnames', int),
])

connect_list_defined_networks_ret = compound('connect_list_defined_networks_ret', [
    ('names', array(string, 16384)),
])

network_lookup_by_uuid_args = compound('network_lookup_by_uuid_args', [
    ('uuid', fopaque(16)),
])

network_lookup_by_uuid_ret = compound('network_lookup_by_uuid_ret', [
    ('net', nonnull_network),
])

network_lookup_by_name_args = compound('network_lookup_by_name_args', [
    ('name', string),
])

network_lookup_by_name_ret = compound('network_lookup_by_name_ret', [
    ('net', nonnull_network),
])

network_create_xml_args = compound('network_create_xml_args', [
    ('xml', string),
])

network_create_xml_ret = compound('network_create_xml_ret', [
    ('net', nonnull_network),
])

network_define_xml_args = compound('network_define_xml_args', [
    ('xml', string),
])

network_define_xml_ret = compound('network_define_xml_ret', [
    ('net', nonnull_network),
])

network_undefine_args = compound('network_undefine_args', [
    ('net', nonnull_network),
])

network_update_args = compound('network_update_args', [
    ('net', nonnull_network),
    ('command', uint),
    ('section', uint),
    ('parentIndex', int),
    ('xml', string),
    ('flags', uint),
])

network_create_args = compound('network_create_args', [
    ('net', nonnull_network),
])

network_destroy_args = compound('network_destroy_args', [
    ('net', nonnull_network),
])

network_get_xml_desc_args = compound('network_get_xml_desc_args', [
    ('net', nonnull_network),
    ('flags', uint),
])

network_get_xml_desc_ret = compound('network_get_xml_desc_ret', [
    ('xml', string),
])

network_get_bridge_name_args = compound('network_get_bridge_name_args', [
    ('net', nonnull_network),
])

network_get_bridge_name_ret = compound('network_get_bridge_name_ret', [
    ('name', string),
])

network_get_autostart_args = compound('network_get_autostart_args', [
    ('net', nonnull_network),
])

network_get_autostart_ret = compound('network_get_autostart_ret', [
    ('autostart', int),
])

network_set_autostart_args = compound('network_set_autostart_args', [
    ('net', nonnull_network),
    ('autostart', int),
])

connect_num_of_nwfilters_ret = compound('connect_num_of_nwfilters_ret', [
    ('num', int),
])

connect_list_nwfilters_args = compound('connect_list_nwfilters_args', [
    ('maxnames', int),
])

connect_list_nwfilters_ret = compound('connect_list_nwfilters_ret', [
    ('names', array(string, 1024)),
])

nwfilter_lookup_by_uuid_args = compound('nwfilter_lookup_by_uuid_args', [
    ('uuid', fopaque(16)),
])

nwfilter_lookup_by_uuid_ret = compound('nwfilter_lookup_by_uuid_ret', [
    ('nwfilter', nonnull_nwfilter),
])

nwfilter_lookup_by_name_args = compound('nwfilter_lookup_by_name_args', [
    ('name', string),
])

nwfilter_lookup_by_name_ret = compound('nwfilter_lookup_by_name_ret', [
    ('nwfilter', nonnull_nwfilter),
])

nwfilter_define_xml_args = compound('nwfilter_define_xml_args', [
    ('xml', string),
])

nwfilter_define_xml_ret = compound('nwfilter_define_xml_ret', [
    ('nwfilter', nonnull_nwfilter),
])

nwfilter_undefine_args = compound('nwfilter_undefine_args', [
    ('nwfilter', nonnull_nwfilter),
])

nwfilter_get_xml_desc_args = compound('nwfilter_get_xml_desc_args', [
    ('nwfilter', nonnull_nwfilter),
    ('flags', uint),
])

nwfilter_get_xml_desc_ret = compound('nwfilter_get_xml_desc_ret', [
    ('xml', string),
])

connect_num_of_interfaces_ret = compound('connect_num_of_interfaces_ret', [
    ('num', int),
])

connect_list_interfaces_args = compound('connect_list_interfaces_args', [
    ('maxnames', int),
])

connect_list_interfaces_ret = compound('connect_list_interfaces_ret', [
    ('names', array(string, 16384)),
])

connect_num_of_defined_interfaces_ret = compound('connect_num_of_defined_interfaces_ret', [
    ('num', int),
])

connect_list_defined_interfaces_args = compound('connect_list_defined_interfaces_args', [
    ('maxnames', int),
])

connect_list_defined_interfaces_ret = compound('connect_list_defined_interfaces_ret', [
    ('names', array(string, 16384)),
])

interface_lookup_by_name_args = compound('interface_lookup_by_name_args', [
    ('name', string),
])

interface_lookup_by_name_ret = compound('interface_lookup_by_name_ret', [
    ('iface', nonnull_interface),
])

interface_lookup_by_mac_string_args = compound('interface_lookup_by_mac_string_args', [
    ('mac', string),
])

interface_lookup_by_mac_string_ret = compound('interface_lookup_by_mac_string_ret', [
    ('iface', nonnull_interface),
])

interface_get_xml_desc_args = compound('interface_get_xml_desc_args', [
    ('iface', nonnull_interface),
    ('flags', uint),
])

interface_get_xml_desc_ret = compound('interface_get_xml_desc_ret', [
    ('xml', string),
])

interface_define_xml_args = compound('interface_define_xml_args', [
    ('xml', string),
    ('flags', uint),
])

interface_define_xml_ret = compound('interface_define_xml_ret', [
    ('iface', nonnull_interface),
])

interface_undefine_args = compound('interface_undefine_args', [
    ('iface', nonnull_interface),
])

interface_create_args = compound('interface_create_args', [
    ('iface', nonnull_interface),
    ('flags', uint),
])

interface_destroy_args = compound('interface_destroy_args', [
    ('iface', nonnull_interface),
    ('flags', uint),
])

interface_change_begin_args = compound('interface_change_begin_args', [
    ('flags', uint),
])

interface_change_commit_args = compound('interface_change_commit_args', [
    ('flags', uint),
])

interface_change_rollback_args = compound('interface_change_rollback_args', [
    ('flags', uint),
])

auth_list_ret = compound('auth_list_ret', [
    ('types', array(auth_type, 20)),
])

auth_sasl_init_ret = compound('auth_sasl_init_ret', [
    ('mechlist', string),
])

auth_sasl_start_args = compound('auth_sasl_start_args', [
    ('mech', string),
    ('nil', int),
    ('data', array(char, 65536)),
])

auth_sasl_start_ret = compound('auth_sasl_start_ret', [
    ('complete', int),
    ('nil', int),
    ('data', array(char, 65536)),
])

auth_sasl_step_args = compound('auth_sasl_step_args', [
    ('nil', int),
    ('data', array(char, 65536)),
])

auth_sasl_step_ret = compound('auth_sasl_step_ret', [
    ('complete', int),
    ('nil', int),
    ('data', array(char, 65536)),
])

auth_polkit_ret = compound('auth_polkit_ret', [
    ('complete', int),
])

connect_num_of_storage_pools_ret = compound('connect_num_of_storage_pools_ret', [
    ('num', int),
])

connect_list_storage_pools_args = compound('connect_list_storage_pools_args', [
    ('maxnames', int),
])

connect_list_storage_pools_ret = compound('connect_list_storage_pools_ret', [
    ('names', array(string, 4096)),
])

connect_num_of_defined_storage_pools_ret = compound('connect_num_of_defined_storage_pools_ret', [
    ('num', int),
])

connect_list_defined_storage_pools_args = compound('connect_list_defined_storage_pools_args', [
    ('maxnames', int),
])

connect_list_defined_storage_pools_ret = compound('connect_list_defined_storage_pools_ret', [
    ('names', array(string, 4096)),
])

connect_find_storage_pool_sources_args = compound('connect_find_storage_pool_sources_args', [
    ('type', string),
    ('srcSpec', optional(string)),
    ('flags', uint),
])

connect_find_storage_pool_sources_ret = compound('connect_find_storage_pool_sources_ret', [
    ('xml', string),
])

storage_pool_lookup_by_uuid_args = compound('storage_pool_lookup_by_uuid_args', [
    ('uuid', fopaque(16)),
])

storage_pool_lookup_by_uuid_ret = compound('storage_pool_lookup_by_uuid_ret', [
    ('pool', nonnull_storage_pool),
])

storage_pool_lookup_by_name_args = compound('storage_pool_lookup_by_name_args', [
    ('name', string),
])

storage_pool_lookup_by_name_ret = compound('storage_pool_lookup_by_name_ret', [
    ('pool', nonnull_storage_pool),
])

storage_pool_lookup_by_volume_args = compound('storage_pool_lookup_by_volume_args', [
    ('vol', nonnull_storage_vol),
])

storage_pool_lookup_by_volume_ret = compound('storage_pool_lookup_by_volume_ret', [
    ('pool', nonnull_storage_pool),
])

storage_pool_create_xml_args = compound('storage_pool_create_xml_args', [
    ('xml', string),
    ('flags', uint),
])

storage_pool_create_xml_ret = compound('storage_pool_create_xml_ret', [
    ('pool', nonnull_storage_pool),
])

storage_pool_define_xml_args = compound('storage_pool_define_xml_args', [
    ('xml', string),
    ('flags', uint),
])

storage_pool_define_xml_ret = compound('storage_pool_define_xml_ret', [
    ('pool', nonnull_storage_pool),
])

storage_pool_build_args = compound('storage_pool_build_args', [
    ('pool', nonnull_storage_pool),
    ('flags', uint),
])

storage_pool_undefine_args = compound('storage_pool_undefine_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_create_args = compound('storage_pool_create_args', [
    ('pool', nonnull_storage_pool),
    ('flags', uint),
])

storage_pool_destroy_args = compound('storage_pool_destroy_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_delete_args = compound('storage_pool_delete_args', [
    ('pool', nonnull_storage_pool),
    ('flags', uint),
])

storage_pool_refresh_args = compound('storage_pool_refresh_args', [
    ('pool', nonnull_storage_pool),
    ('flags', uint),
])

storage_pool_get_xml_desc_args = compound('storage_pool_get_xml_desc_args', [
    ('pool', nonnull_storage_pool),
    ('flags', uint),
])

storage_pool_get_xml_desc_ret = compound('storage_pool_get_xml_desc_ret', [
    ('xml', string),
])

storage_pool_get_info_args = compound('storage_pool_get_info_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_get_info_ret = compound('storage_pool_get_info_ret', [
    ('state', uchar),
    ('capacity', uhyper),
    ('allocation', uhyper),
    ('available', uhyper),
])

storage_pool_get_autostart_args = compound('storage_pool_get_autostart_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_get_autostart_ret = compound('storage_pool_get_autostart_ret', [
    ('autostart', int),
])

storage_pool_set_autostart_args = compound('storage_pool_set_autostart_args', [
    ('pool', nonnull_storage_pool),
    ('autostart', int),
])

storage_pool_num_of_volumes_args = compound('storage_pool_num_of_volumes_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_num_of_volumes_ret = compound('storage_pool_num_of_volumes_ret', [
    ('num', int),
])

storage_pool_list_volumes_args = compound('storage_pool_list_volumes_args', [
    ('pool', nonnull_storage_pool),
    ('maxnames', int),
])

storage_pool_list_volumes_ret = compound('storage_pool_list_volumes_ret', [
    ('names', array(string, 16384)),
])

storage_vol_lookup_by_name_args = compound('storage_vol_lookup_by_name_args', [
    ('pool', nonnull_storage_pool),
    ('name', string),
])

storage_vol_lookup_by_name_ret = compound('storage_vol_lookup_by_name_ret', [
    ('vol', nonnull_storage_vol),
])

storage_vol_lookup_by_key_args = compound('storage_vol_lookup_by_key_args', [
    ('key', string),
])

storage_vol_lookup_by_key_ret = compound('storage_vol_lookup_by_key_ret', [
    ('vol', nonnull_storage_vol),
])

storage_vol_lookup_by_path_args = compound('storage_vol_lookup_by_path_args', [
    ('path', string),
])

storage_vol_lookup_by_path_ret = compound('storage_vol_lookup_by_path_ret', [
    ('vol', nonnull_storage_vol),
])

storage_vol_create_xml_args = compound('storage_vol_create_xml_args', [
    ('pool', nonnull_storage_pool),
    ('xml', string),
    ('flags', uint),
])

storage_vol_create_xml_ret = compound('storage_vol_create_xml_ret', [
    ('vol', nonnull_storage_vol),
])

storage_vol_create_xml_from_args = compound('storage_vol_create_xml_from_args', [
    ('pool', nonnull_storage_pool),
    ('xml', string),
    ('clonevol', nonnull_storage_vol),
    ('flags', uint),
])

storage_vol_create_xml_from_ret = compound('storage_vol_create_xml_from_ret', [
    ('vol', nonnull_storage_vol),
])

storage_vol_delete_args = compound('storage_vol_delete_args', [
    ('vol', nonnull_storage_vol),
    ('flags', uint),
])

storage_vol_wipe_args = compound('storage_vol_wipe_args', [
    ('vol', nonnull_storage_vol),
    ('flags', uint),
])

storage_vol_wipe_pattern_args = compound('storage_vol_wipe_pattern_args', [
    ('vol', nonnull_storage_vol),
    ('algorithm', uint),
    ('flags', uint),
])

storage_vol_get_xml_desc_args = compound('storage_vol_get_xml_desc_args', [
    ('vol', nonnull_storage_vol),
    ('flags', uint),
])

storage_vol_get_xml_desc_ret = compound('storage_vol_get_xml_desc_ret', [
    ('xml', string),
])

storage_vol_get_info_args = compound('storage_vol_get_info_args', [
    ('vol', nonnull_storage_vol),
])

storage_vol_get_info_ret = compound('storage_vol_get_info_ret', [
    ('type', char),
    ('capacity', uhyper),
    ('allocation', uhyper),
])

storage_vol_get_path_args = compound('storage_vol_get_path_args', [
    ('vol', nonnull_storage_vol),
])

storage_vol_get_path_ret = compound('storage_vol_get_path_ret', [
    ('name', string),
])

storage_vol_resize_args = compound('storage_vol_resize_args', [
    ('vol', nonnull_storage_vol),
    ('capacity', uhyper),
    ('flags', uint),
])

node_num_of_devices_args = compound('node_num_of_devices_args', [
    ('cap', optional(string)),
    ('flags', uint),
])

node_num_of_devices_ret = compound('node_num_of_devices_ret', [
    ('num', int),
])

node_list_devices_args = compound('node_list_devices_args', [
    ('cap', optional(string)),
    ('maxnames', int),
    ('flags', uint),
])

node_list_devices_ret = compound('node_list_devices_ret', [
    ('names', array(string, 16384)),
])

node_device_lookup_by_name_args = compound('node_device_lookup_by_name_args', [
    ('name', string),
])

node_device_lookup_by_name_ret = compound('node_device_lookup_by_name_ret', [
    ('dev', nonnull_node_device),
])

node_device_lookup_scsi_host_by_wwn_args = compound('node_device_lookup_scsi_host_by_wwn_args', [
    ('wwnn', string),
    ('wwpn', string),
    ('flags', uint),
])

node_device_lookup_scsi_host_by_wwn_ret = compound('node_device_lookup_scsi_host_by_wwn_ret', [
    ('dev', nonnull_node_device),
])

node_device_get_xml_desc_args = compound('node_device_get_xml_desc_args', [
    ('name', string),
    ('flags', uint),
])

node_device_get_xml_desc_ret = compound('node_device_get_xml_desc_ret', [
    ('xml', string),
])

node_device_get_parent_args = compound('node_device_get_parent_args', [
    ('name', string),
])

node_device_get_parent_ret = compound('node_device_get_parent_ret', [
    ('parent', optional(string)),
])

node_device_num_of_caps_args = compound('node_device_num_of_caps_args', [
    ('name', string),
])

node_device_num_of_caps_ret = compound('node_device_num_of_caps_ret', [
    ('num', int),
])

node_device_list_caps_args = compound('node_device_list_caps_args', [
    ('name', string),
    ('maxnames', int),
])

node_device_list_caps_ret = compound('node_device_list_caps_ret', [
    ('names', array(string, 65536)),
])

node_device_dettach_args = compound('node_device_dettach_args', [
    ('name', string),
])

node_device_detach_flags_args = compound('node_device_detach_flags_args', [
    ('name', string),
    ('driverName', optional(string)),
    ('flags', uint),
])

node_device_re_attach_args = compound('node_device_re_attach_args', [
    ('name', string),
])

node_device_reset_args = compound('node_device_reset_args', [
    ('name', string),
])

node_device_create_xml_args = compound('node_device_create_xml_args', [
    ('xml_desc', string),
    ('flags', uint),
])

node_device_create_xml_ret = compound('node_device_create_xml_ret', [
    ('dev', nonnull_node_device),
])

node_device_destroy_args = compound('node_device_destroy_args', [
    ('name', string),
])

connect_domain_event_register_ret = compound('connect_domain_event_register_ret', [
    ('cb_registered', int),
])

connect_domain_event_deregister_ret = compound('connect_domain_event_deregister_ret', [
    ('cb_registered', int),
])

domain_event_lifecycle_msg = compound('domain_event_lifecycle_msg', [
    ('dom', nonnull_domain),
    ('event', int),
    ('detail', int),
])

connect_domain_xml_from_native_args = compound('connect_domain_xml_from_native_args', [
    ('nativeFormat', string),
    ('nativeConfig', string),
    ('flags', uint),
])

connect_domain_xml_from_native_ret = compound('connect_domain_xml_from_native_ret', [
    ('domainXml', string),
])

connect_domain_xml_to_native_args = compound('connect_domain_xml_to_native_args', [
    ('nativeFormat', string),
    ('domainXml', string),
    ('flags', uint),
])

connect_domain_xml_to_native_ret = compound('connect_domain_xml_to_native_ret', [
    ('nativeConfig', string),
])

connect_num_of_secrets_ret = compound('connect_num_of_secrets_ret', [
    ('num', int),
])

connect_list_secrets_args = compound('connect_list_secrets_args', [
    ('maxuuids', int),
])

connect_list_secrets_ret = compound('connect_list_secrets_ret', [
    ('uuids', array(string, 16384)),
])

secret_lookup_by_uuid_args = compound('secret_lookup_by_uuid_args', [
    ('uuid', fopaque(16)),
])

secret_lookup_by_uuid_ret = compound('secret_lookup_by_uuid_ret', [
    ('secret', nonnull_secret),
])

secret_define_xml_args = compound('secret_define_xml_args', [
    ('xml', string),
    ('flags', uint),
])

secret_define_xml_ret = compound('secret_define_xml_ret', [
    ('secret', nonnull_secret),
])

secret_get_xml_desc_args = compound('secret_get_xml_desc_args', [
    ('secret', nonnull_secret),
    ('flags', uint),
])

secret_get_xml_desc_ret = compound('secret_get_xml_desc_ret', [
    ('xml', string),
])

secret_set_value_args = compound('secret_set_value_args', [
    ('secret', nonnull_secret),
    ('value', opaque),
    ('flags', uint),
])

secret_get_value_args = compound('secret_get_value_args', [
    ('secret', nonnull_secret),
    ('flags', uint),
])

secret_get_value_ret = compound('secret_get_value_ret', [
    ('value', opaque),
])

secret_undefine_args = compound('secret_undefine_args', [
    ('secret', nonnull_secret),
])

secret_lookup_by_usage_args = compound('secret_lookup_by_usage_args', [
    ('usageType', int),
    ('usageID', string),
])

secret_lookup_by_usage_ret = compound('secret_lookup_by_usage_ret', [
    ('secret', nonnull_secret),
])

domain_migrate_prepare_tunnel_args = compound('domain_migrate_prepare_tunnel_args', [
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
    ('dom_xml', string),
])

connect_is_secure_ret = compound('connect_is_secure_ret', [
    ('secure', int),
])

domain_is_active_args = compound('domain_is_active_args', [
    ('dom', nonnull_domain),
])

domain_is_active_ret = compound('domain_is_active_ret', [
    ('active', int),
])

domain_is_persistent_args = compound('domain_is_persistent_args', [
    ('dom', nonnull_domain),
])

domain_is_persistent_ret = compound('domain_is_persistent_ret', [
    ('persistent', int),
])

domain_is_updated_args = compound('domain_is_updated_args', [
    ('dom', nonnull_domain),
])

domain_is_updated_ret = compound('domain_is_updated_ret', [
    ('updated', int),
])

network_is_active_args = compound('network_is_active_args', [
    ('net', nonnull_network),
])

network_is_active_ret = compound('network_is_active_ret', [
    ('active', int),
])

network_is_persistent_args = compound('network_is_persistent_args', [
    ('net', nonnull_network),
])

network_is_persistent_ret = compound('network_is_persistent_ret', [
    ('persistent', int),
])

storage_pool_is_active_args = compound('storage_pool_is_active_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_is_active_ret = compound('storage_pool_is_active_ret', [
    ('active', int),
])

storage_pool_is_persistent_args = compound('storage_pool_is_persistent_args', [
    ('pool', nonnull_storage_pool),
])

storage_pool_is_persistent_ret = compound('storage_pool_is_persistent_ret', [
    ('persistent', int),
])

interface_is_active_args = compound('interface_is_active_args', [
    ('iface', nonnull_interface),
])

interface_is_active_ret = compound('interface_is_active_ret', [
    ('active', int),
])

connect_compare_cpu_args = compound('connect_compare_cpu_args', [
    ('xml', string),
    ('flags', uint),
])

connect_compare_cpu_ret = compound('connect_compare_cpu_ret', [
    ('result', int),
])

connect_baseline_cpu_args = compound('connect_baseline_cpu_args', [
    ('xmlCPUs', array(string, 256)),
    ('flags', uint),
])

connect_baseline_cpu_ret = compound('connect_baseline_cpu_ret', [
    ('cpu', string),
])

domain_get_job_info_args = compound('domain_get_job_info_args', [
    ('dom', nonnull_domain),
])

domain_get_job_info_ret = compound('domain_get_job_info_ret', [
    ('type', int),
    ('timeElapsed', uhyper),
    ('timeRemaining', uhyper),
    ('dataTotal', uhyper),
    ('dataProcessed', uhyper),
    ('dataRemaining', uhyper),
    ('memTotal', uhyper),
    ('memProcessed', uhyper),
    ('memRemaining', uhyper),
    ('fileTotal', uhyper),
    ('fileProcessed', uhyper),
    ('fileRemaining', uhyper),
])

domain_get_job_stats_args = compound('domain_get_job_stats_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_job_stats_ret = compound('domain_get_job_stats_ret', [
    ('type', int),
    ('params', array(typed_param, 64)),
])

domain_abort_job_args = compound('domain_abort_job_args', [
    ('dom', nonnull_domain),
])

domain_migrate_set_max_downtime_args = compound('domain_migrate_set_max_downtime_args', [
    ('dom', nonnull_domain),
    ('downtime', uhyper),
    ('flags', uint),
])

domain_migrate_get_compression_cache_args = compound('domain_migrate_get_compression_cache_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_migrate_get_compression_cache_ret = compound('domain_migrate_get_compression_cache_ret', [
    ('cacheSize', uhyper),
])

domain_migrate_set_compression_cache_args = compound('domain_migrate_set_compression_cache_args', [
    ('dom', nonnull_domain),
    ('cacheSize', uhyper),
    ('flags', uint),
])

domain_migrate_set_max_speed_args = compound('domain_migrate_set_max_speed_args', [
    ('dom', nonnull_domain),
    ('bandwidth', uhyper),
    ('flags', uint),
])

domain_migrate_get_max_speed_args = compound('domain_migrate_get_max_speed_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_migrate_get_max_speed_ret = compound('domain_migrate_get_max_speed_ret', [
    ('bandwidth', uhyper),
])

connect_domain_event_register_any_args = compound('connect_domain_event_register_any_args', [
    ('eventID', int),
])

connect_domain_event_deregister_any_args = compound('connect_domain_event_deregister_any_args', [
    ('eventID', int),
])

domain_event_reboot_msg = compound('domain_event_reboot_msg', [
    ('dom', nonnull_domain),
])

domain_event_rtc_change_msg = compound('domain_event_rtc_change_msg', [
    ('dom', nonnull_domain),
    ('offset', hyper),
])

domain_event_watchdog_msg = compound('domain_event_watchdog_msg', [
    ('dom', nonnull_domain),
    ('action', int),
])

domain_event_io_error_msg = compound('domain_event_io_error_msg', [
    ('dom', nonnull_domain),
    ('srcPath', string),
    ('devAlias', string),
    ('action', int),
])

domain_event_io_error_reason_msg = compound('domain_event_io_error_reason_msg', [
    ('dom', nonnull_domain),
    ('srcPath', string),
    ('devAlias', string),
    ('action', int),
    ('reason', string),
])

domain_event_graphics_address = compound('domain_event_graphics_address', [
    ('family', int),
    ('node', string),
    ('service', string),
])

domain_event_graphics_identity = compound('domain_event_graphics_identity', [
    ('type', string),
    ('name', string),
])

domain_event_graphics_msg = compound('domain_event_graphics_msg', [
    ('dom', nonnull_domain),
    ('phase', int),
    ('local', domain_event_graphics_address),
    ('remote', domain_event_graphics_address),
    ('authScheme', string),
    ('subject', array(domain_event_graphics_identity, 20)),
])

domain_event_block_job_msg = compound('domain_event_block_job_msg', [
    ('dom', nonnull_domain),
    ('path', string),
    ('type', int),
    ('status', int),
])

domain_event_disk_change_msg = compound('domain_event_disk_change_msg', [
    ('dom', nonnull_domain),
    ('oldSrcPath', optional(string)),
    ('newSrcPath', optional(string)),
    ('devAlias', string),
    ('reason', int),
])

domain_event_tray_change_msg = compound('domain_event_tray_change_msg', [
    ('dom', nonnull_domain),
    ('devAlias', string),
    ('reason', int),
])

domain_event_pmwakeup_msg = compound('domain_event_pmwakeup_msg', [
    ('dom', nonnull_domain),
])

domain_event_pmsuspend_msg = compound('domain_event_pmsuspend_msg', [
    ('dom', nonnull_domain),
])

domain_event_balloon_change_msg = compound('domain_event_balloon_change_msg', [
    ('dom', nonnull_domain),
    ('actual', uhyper),
])

domain_event_pmsuspend_disk_msg = compound('domain_event_pmsuspend_disk_msg', [
    ('dom', nonnull_domain),
])

domain_managed_save_args = compound('domain_managed_save_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_has_managed_save_image_args = compound('domain_has_managed_save_image_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_has_managed_save_image_ret = compound('domain_has_managed_save_image_ret', [
    ('result', int),
])

domain_managed_save_remove_args = compound('domain_managed_save_remove_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_snapshot_create_xml_args = compound('domain_snapshot_create_xml_args', [
    ('dom', nonnull_domain),
    ('xml_desc', string),
    ('flags', uint),
])

domain_snapshot_create_xml_ret = compound('domain_snapshot_create_xml_ret', [
    ('snap', nonnull_domain_snapshot),
])

domain_snapshot_get_xml_desc_args = compound('domain_snapshot_get_xml_desc_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_snapshot_get_xml_desc_ret = compound('domain_snapshot_get_xml_desc_ret', [
    ('xml', string),
])

domain_snapshot_num_args = compound('domain_snapshot_num_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_snapshot_num_ret = compound('domain_snapshot_num_ret', [
    ('num', int),
])

domain_snapshot_list_names_args = compound('domain_snapshot_list_names_args', [
    ('dom', nonnull_domain),
    ('maxnames', int),
    ('flags', uint),
])

domain_snapshot_list_names_ret = compound('domain_snapshot_list_names_ret', [
    ('names', array(string, 1024)),
])

domain_list_all_snapshots_args = compound('domain_list_all_snapshots_args', [
    ('dom', nonnull_domain),
    ('need_results', int),
    ('flags', uint),
])

domain_list_all_snapshots_ret = compound('domain_list_all_snapshots_ret', [
    ('snapshots', array(nonnull_domain_snapshot, 1024)),
    ('ret', int),
])

domain_snapshot_num_children_args = compound('domain_snapshot_num_children_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_snapshot_num_children_ret = compound('domain_snapshot_num_children_ret', [
    ('num', int),
])

domain_snapshot_list_children_names_args = compound('domain_snapshot_list_children_names_args', [
    ('snap', nonnull_domain_snapshot),
    ('maxnames', int),
    ('flags', uint),
])

domain_snapshot_list_children_names_ret = compound('domain_snapshot_list_children_names_ret', [
    ('names', array(string, 1024)),
])

domain_snapshot_list_all_children_args = compound('domain_snapshot_list_all_children_args', [
    ('snapshot', nonnull_domain_snapshot),
    ('need_results', int),
    ('flags', uint),
])

domain_snapshot_list_all_children_ret = compound('domain_snapshot_list_all_children_ret', [
    ('snapshots', array(nonnull_domain_snapshot, 1024)),
    ('ret', int),
])

domain_snapshot_lookup_by_name_args = compound('domain_snapshot_lookup_by_name_args', [
    ('dom', nonnull_domain),
    ('name', string),
    ('flags', uint),
])

domain_snapshot_lookup_by_name_ret = compound('domain_snapshot_lookup_by_name_ret', [
    ('snap', nonnull_domain_snapshot),
])

domain_has_current_snapshot_args = compound('domain_has_current_snapshot_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_has_current_snapshot_ret = compound('domain_has_current_snapshot_ret', [
    ('result', int),
])

domain_snapshot_get_parent_args = compound('domain_snapshot_get_parent_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_snapshot_get_parent_ret = compound('domain_snapshot_get_parent_ret', [
    ('snap', nonnull_domain_snapshot),
])

domain_snapshot_current_args = compound('domain_snapshot_current_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_snapshot_current_ret = compound('domain_snapshot_current_ret', [
    ('snap', nonnull_domain_snapshot),
])

domain_snapshot_is_current_args = compound('domain_snapshot_is_current_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_snapshot_is_current_ret = compound('domain_snapshot_is_current_ret', [
    ('current', int),
])

domain_snapshot_has_metadata_args = compound('domain_snapshot_has_metadata_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_snapshot_has_metadata_ret = compound('domain_snapshot_has_metadata_ret', [
    ('metadata', int),
])

domain_revert_to_snapshot_args = compound('domain_revert_to_snapshot_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_snapshot_delete_args = compound('domain_snapshot_delete_args', [
    ('snap', nonnull_domain_snapshot),
    ('flags', uint),
])

domain_open_console_args = compound('domain_open_console_args', [
    ('dom', nonnull_domain),
    ('dev_name', optional(string)),
    ('flags', uint),
])

domain_open_channel_args = compound('domain_open_channel_args', [
    ('dom', nonnull_domain),
    ('name', optional(string)),
    ('flags', uint),
])

storage_vol_upload_args = compound('storage_vol_upload_args', [
    ('vol', nonnull_storage_vol),
    ('offset', uhyper),
    ('length', uhyper),
    ('flags', uint),
])

storage_vol_download_args = compound('storage_vol_download_args', [
    ('vol', nonnull_storage_vol),
    ('offset', uhyper),
    ('length', uhyper),
    ('flags', uint),
])

domain_get_state_args = compound('domain_get_state_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_state_ret = compound('domain_get_state_ret', [
    ('state', int),
    ('reason', int),
])

domain_migrate_begin3_args = compound('domain_migrate_begin3_args', [
    ('dom', nonnull_domain),
    ('xmlin', optional(string)),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
])

domain_migrate_begin3_ret = compound('domain_migrate_begin3_ret', [
    ('cookie_out', opaque),
    ('xml', string),
])

domain_migrate_prepare3_args = compound('domain_migrate_prepare3_args', [
    ('cookie_in', opaque),
    ('uri_in', optional(string)),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
    ('dom_xml', string),
])

domain_migrate_prepare3_ret = compound('domain_migrate_prepare3_ret', [
    ('cookie_out', opaque),
    ('uri_out', optional(string)),
])

domain_migrate_prepare_tunnel3_args = compound('domain_migrate_prepare_tunnel3_args', [
    ('cookie_in', opaque),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
    ('dom_xml', string),
])

domain_migrate_prepare_tunnel3_ret = compound('domain_migrate_prepare_tunnel3_ret', [
    ('cookie_out', opaque),
])

domain_migrate_perform3_args = compound('domain_migrate_perform3_args', [
    ('dom', nonnull_domain),
    ('xmlin', optional(string)),
    ('cookie_in', opaque),
    ('dconnuri', optional(string)),
    ('uri', optional(string)),
    ('flags', uhyper),
    ('dname', optional(string)),
    ('resource', uhyper),
])

domain_migrate_perform3_ret = compound('domain_migrate_perform3_ret', [
    ('cookie_out', opaque),
])

domain_migrate_finish3_args = compound('domain_migrate_finish3_args', [
    ('dname', string),
    ('cookie_in', opaque),
    ('dconnuri', optional(string)),
    ('uri', optional(string)),
    ('flags', uhyper),
    ('cancelled', int),
])

domain_migrate_finish3_ret = compound('domain_migrate_finish3_ret', [
    ('dom', nonnull_domain),
    ('cookie_out', opaque),
])

domain_migrate_confirm3_args = compound('domain_migrate_confirm3_args', [
    ('dom', nonnull_domain),
    ('cookie_in', opaque),
    ('flags', uhyper),
    ('cancelled', int),
])

domain_event_control_error_msg = compound('domain_event_control_error_msg', [
    ('dom', nonnull_domain),
])

domain_get_control_info_args = compound('domain_get_control_info_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_control_info_ret = compound('domain_get_control_info_ret', [
    ('state', uint),
    ('details', uint),
    ('stateTime', uhyper),
])

domain_open_graphics_args = compound('domain_open_graphics_args', [
    ('dom', nonnull_domain),
    ('idx', uint),
    ('flags', uint),
])

node_suspend_for_duration_args = compound('node_suspend_for_duration_args', [
    ('target', uint),
    ('duration', uhyper),
    ('flags', uint),
])

domain_shutdown_flags_args = compound('domain_shutdown_flags_args', [
    ('dom', nonnull_domain),
    ('flags', uint),
])

domain_get_disk_errors_args = compound('domain_get_disk_errors_args', [
    ('dom', nonnull_domain),
    ('maxerrors', uint),
    ('flags', uint),
])

domain_get_disk_errors_ret = compound('domain_get_disk_errors_ret', [
    ('errors', array(domain_disk_error, 256)),
    ('nerrors', int),
])

connect_list_all_domains_args = compound('connect_list_all_domains_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_domains_ret = compound('connect_list_all_domains_ret', [
    ('domains', array(nonnull_domain, 16384)),
    ('ret', uint),
])

connect_list_all_storage_pools_args = compound('connect_list_all_storage_pools_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_storage_pools_ret = compound('connect_list_all_storage_pools_ret', [
    ('pools', array(nonnull_storage_pool, 4096)),
    ('ret', uint),
])

storage_pool_list_all_volumes_args = compound('storage_pool_list_all_volumes_args', [
    ('pool', nonnull_storage_pool),
    ('need_results', int),
    ('flags', uint),
])

storage_pool_list_all_volumes_ret = compound('storage_pool_list_all_volumes_ret', [
    ('vols', array(nonnull_storage_vol, 16384)),
    ('ret', uint),
])

connect_list_all_networks_args = compound('connect_list_all_networks_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_networks_ret = compound('connect_list_all_networks_ret', [
    ('nets', array(nonnull_network, 16384)),
    ('ret', uint),
])

connect_list_all_interfaces_args = compound('connect_list_all_interfaces_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_interfaces_ret = compound('connect_list_all_interfaces_ret', [
    ('ifaces', array(nonnull_interface, 16384)),
    ('ret', uint),
])

connect_list_all_node_devices_args = compound('connect_list_all_node_devices_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_node_devices_ret = compound('connect_list_all_node_devices_ret', [
    ('devices', array(nonnull_node_device, 16384)),
    ('ret', uint),
])

connect_list_all_nwfilters_args = compound('connect_list_all_nwfilters_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_nwfilters_ret = compound('connect_list_all_nwfilters_ret', [
    ('filters', array(nonnull_nwfilter, 1024)),
    ('ret', uint),
])

connect_list_all_secrets_args = compound('connect_list_all_secrets_args', [
    ('need_results', int),
    ('flags', uint),
])

connect_list_all_secrets_ret = compound('connect_list_all_secrets_ret', [
    ('secrets', array(nonnull_secret, 16384)),
    ('ret', uint),
])

node_set_memory_parameters_args = compound('node_set_memory_parameters_args', [
    ('params', array(typed_param, 64)),
    ('flags', uint),
])

node_get_memory_parameters_args = compound('node_get_memory_parameters_args', [
    ('nparams', int),
    ('flags', uint),
])

node_get_memory_parameters_ret = compound('node_get_memory_parameters_ret', [
    ('params', array(typed_param, 64)),
    ('nparams', int),
])

node_get_cpu_map_args = compound('node_get_cpu_map_args', [
    ('need_map', int),
    ('need_online', int),
    ('flags', uint),
])

node_get_cpu_map_ret = compound('node_get_cpu_map_ret', [
    ('cpumap', opaque),
    ('online', uint),
    ('ret', int),
])

domain_fstrim_args = compound('domain_fstrim_args', [
    ('dom', nonnull_domain),
    ('mountPoint', optional(string)),
    ('minimum', uhyper),
    ('flags', uint),
])

domain_migrate_begin3_params_args = compound('domain_migrate_begin3_params_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 64)),
    ('flags', uint),
])

domain_migrate_begin3_params_ret = compound('domain_migrate_begin3_params_ret', [
    ('cookie_out', opaque),
    ('xml', string),
])

domain_migrate_prepare3_params_args = compound('domain_migrate_prepare3_params_args', [
    ('params', array(typed_param, 64)),
    ('cookie_in', opaque),
    ('flags', uint),
])

domain_migrate_prepare3_params_ret = compound('domain_migrate_prepare3_params_ret', [
    ('cookie_out', opaque),
    ('uri_out', optional(string)),
])

domain_migrate_prepare_tunnel3_params_args = compound('domain_migrate_prepare_tunnel3_params_args', [
    ('params', array(typed_param, 64)),
    ('cookie_in', opaque),
    ('flags', uint),
])

domain_migrate_prepare_tunnel3_params_ret = compound('domain_migrate_prepare_tunnel3_params_ret', [
    ('cookie_out', opaque),
])

domain_migrate_perform3_params_args = compound('domain_migrate_perform3_params_args', [
    ('dom', nonnull_domain),
    ('dconnuri', optional(string)),
    ('params', array(typed_param, 64)),
    ('cookie_in', opaque),
    ('flags', uint),
])

domain_migrate_perform3_params_ret = compound('domain_migrate_perform3_params_ret', [
    ('cookie_out', opaque),
])

domain_migrate_finish3_params_args = compound('domain_migrate_finish3_params_args', [
    ('params', array(typed_param, 64)),
    ('cookie_in', opaque),
    ('flags', uint),
    ('cancelled', int),
])

domain_migrate_finish3_params_ret = compound('domain_migrate_finish3_params_ret', [
    ('dom', nonnull_domain),
    ('cookie_out', opaque),
])

domain_migrate_confirm3_params_args = compound('domain_migrate_confirm3_params_args', [
    ('dom', nonnull_domain),
    ('params', array(typed_param, 64)),
    ('cookie_in', opaque),
    ('flags', uint),
    ('cancelled', int),
])

domain_event_device_removed_msg = compound('domain_event_device_removed_msg', [
    ('dom', nonnull_domain),
    ('devAlias', string),
])

connect_get_cpu_model_names_args = compound('connect_get_cpu_model_names_args', [
    ('arch', string),
    ('need_results', int),
    ('flags', uint),
])

connect_get_cpu_model_names_ret = compound('connect_get_cpu_model_names_ret', [
    ('models', array(string, 8192)),
    ('ret', int),
])

class ConnectOpen(ProcedureBase):
    id = 1
    name = 'connect_open'
    args = connect_open_args
    ret = None

class ConnectClose(ProcedureBase):
    id = 2
    name = 'connect_close'
    args = None
    ret = None

class ConnectGetType(ProcedureBase):
    id = 3
    name = 'connect_get_type'
    args = None
    ret = connect_get_type_ret

class ConnectGetVersion(ProcedureBase):
    id = 4
    name = 'connect_get_version'
    args = None
    ret = connect_get_version_ret

class ConnectGetMaxVcpus(ProcedureBase):
    id = 5
    name = 'connect_get_max_vcpus'
    args = connect_get_max_vcpus_args
    ret = connect_get_max_vcpus_ret

class NodeGetInfo(ProcedureBase):
    id = 6
    name = 'node_get_info'
    args = None
    ret = node_get_info_ret

class ConnectGetCapabilities(ProcedureBase):
    id = 7
    name = 'connect_get_capabilities'
    args = None
    ret = connect_get_capabilities_ret

class DomainAttachDevice(ProcedureBase):
    id = 8
    name = 'domain_attach_device'
    args = domain_attach_device_args
    ret = None

class DomainCreate(ProcedureBase):
    id = 9
    name = 'domain_create'
    args = domain_create_args
    ret = None

class DomainCreateXml(ProcedureBase):
    id = 10
    name = 'domain_create_xml'
    args = domain_create_xml_args
    ret = domain_create_xml_ret

class DomainDefineXml(ProcedureBase):
    id = 11
    name = 'domain_define_xml'
    args = domain_define_xml_args
    ret = domain_define_xml_ret

class DomainDestroy(ProcedureBase):
    id = 12
    name = 'domain_destroy'
    args = domain_destroy_args
    ret = None

class DomainDetachDevice(ProcedureBase):
    id = 13
    name = 'domain_detach_device'
    args = domain_detach_device_args
    ret = None

class DomainGetXmlDesc(ProcedureBase):
    id = 14
    name = 'domain_get_xml_desc'
    args = domain_get_xml_desc_args
    ret = domain_get_xml_desc_ret

class DomainGetAutostart(ProcedureBase):
    id = 15
    name = 'domain_get_autostart'
    args = domain_get_autostart_args
    ret = domain_get_autostart_ret

class DomainGetInfo(ProcedureBase):
    id = 16
    name = 'domain_get_info'
    args = domain_get_info_args
    ret = domain_get_info_ret

class DomainGetMaxMemory(ProcedureBase):
    id = 17
    name = 'domain_get_max_memory'
    args = domain_get_max_memory_args
    ret = domain_get_max_memory_ret

class DomainGetMaxVcpus(ProcedureBase):
    id = 18
    name = 'domain_get_max_vcpus'
    args = domain_get_max_vcpus_args
    ret = domain_get_max_vcpus_ret

class DomainGetOsType(ProcedureBase):
    id = 19
    name = 'domain_get_os_type'
    args = domain_get_os_type_args
    ret = domain_get_os_type_ret

class DomainGetVcpus(ProcedureBase):
    id = 20
    name = 'domain_get_vcpus'
    args = domain_get_vcpus_args
    ret = domain_get_vcpus_ret

class ConnectListDefinedDomains(ProcedureBase):
    id = 21
    name = 'connect_list_defined_domains'
    args = connect_list_defined_domains_args
    ret = connect_list_defined_domains_ret

class DomainLookupById(ProcedureBase):
    id = 22
    name = 'domain_lookup_by_id'
    args = domain_lookup_by_id_args
    ret = domain_lookup_by_id_ret

class DomainLookupByName(ProcedureBase):
    id = 23
    name = 'domain_lookup_by_name'
    args = domain_lookup_by_name_args
    ret = domain_lookup_by_name_ret

class DomainLookupByUuid(ProcedureBase):
    id = 24
    name = 'domain_lookup_by_uuid'
    args = domain_lookup_by_uuid_args
    ret = domain_lookup_by_uuid_ret

class ConnectNumOfDefinedDomains(ProcedureBase):
    id = 25
    name = 'connect_num_of_defined_domains'
    args = None
    ret = connect_num_of_defined_domains_ret

class DomainPinVcpu(ProcedureBase):
    id = 26
    name = 'domain_pin_vcpu'
    args = domain_pin_vcpu_args
    ret = None

class DomainReboot(ProcedureBase):
    id = 27
    name = 'domain_reboot'
    args = domain_reboot_args
    ret = None

class DomainResume(ProcedureBase):
    id = 28
    name = 'domain_resume'
    args = domain_resume_args
    ret = None

class DomainSetAutostart(ProcedureBase):
    id = 29
    name = 'domain_set_autostart'
    args = domain_set_autostart_args
    ret = None

class DomainSetMaxMemory(ProcedureBase):
    id = 30
    name = 'domain_set_max_memory'
    args = domain_set_max_memory_args
    ret = None

class DomainSetMemory(ProcedureBase):
    id = 31
    name = 'domain_set_memory'
    args = domain_set_memory_args
    ret = None

class DomainSetVcpus(ProcedureBase):
    id = 32
    name = 'domain_set_vcpus'
    args = domain_set_vcpus_args
    ret = None

class DomainShutdown(ProcedureBase):
    id = 33
    name = 'domain_shutdown'
    args = domain_shutdown_args
    ret = None

class DomainSuspend(ProcedureBase):
    id = 34
    name = 'domain_suspend'
    args = domain_suspend_args
    ret = None

class DomainUndefine(ProcedureBase):
    id = 35
    name = 'domain_undefine'
    args = domain_undefine_args
    ret = None

class ConnectListDefinedNetworks(ProcedureBase):
    id = 36
    name = 'connect_list_defined_networks'
    args = connect_list_defined_networks_args
    ret = connect_list_defined_networks_ret

class ConnectListDomains(ProcedureBase):
    id = 37
    name = 'connect_list_domains'
    args = connect_list_domains_args
    ret = connect_list_domains_ret

class ConnectListNetworks(ProcedureBase):
    id = 38
    name = 'connect_list_networks'
    args = connect_list_networks_args
    ret = connect_list_networks_ret

class NetworkCreate(ProcedureBase):
    id = 39
    name = 'network_create'
    args = network_create_args
    ret = None

class NetworkCreateXml(ProcedureBase):
    id = 40
    name = 'network_create_xml'
    args = network_create_xml_args
    ret = network_create_xml_ret

class NetworkDefineXml(ProcedureBase):
    id = 41
    name = 'network_define_xml'
    args = network_define_xml_args
    ret = network_define_xml_ret

class NetworkDestroy(ProcedureBase):
    id = 42
    name = 'network_destroy'
    args = network_destroy_args
    ret = None

class NetworkGetXmlDesc(ProcedureBase):
    id = 43
    name = 'network_get_xml_desc'
    args = network_get_xml_desc_args
    ret = network_get_xml_desc_ret

class NetworkGetAutostart(ProcedureBase):
    id = 44
    name = 'network_get_autostart'
    args = network_get_autostart_args
    ret = network_get_autostart_ret

class NetworkGetBridgeName(ProcedureBase):
    id = 45
    name = 'network_get_bridge_name'
    args = network_get_bridge_name_args
    ret = network_get_bridge_name_ret

class NetworkLookupByName(ProcedureBase):
    id = 46
    name = 'network_lookup_by_name'
    args = network_lookup_by_name_args
    ret = network_lookup_by_name_ret

class NetworkLookupByUuid(ProcedureBase):
    id = 47
    name = 'network_lookup_by_uuid'
    args = network_lookup_by_uuid_args
    ret = network_lookup_by_uuid_ret

class NetworkSetAutostart(ProcedureBase):
    id = 48
    name = 'network_set_autostart'
    args = network_set_autostart_args
    ret = None

class NetworkUndefine(ProcedureBase):
    id = 49
    name = 'network_undefine'
    args = network_undefine_args
    ret = None

class ConnectNumOfDefinedNetworks(ProcedureBase):
    id = 50
    name = 'connect_num_of_defined_networks'
    args = None
    ret = connect_num_of_defined_networks_ret

class ConnectNumOfDomains(ProcedureBase):
    id = 51
    name = 'connect_num_of_domains'
    args = None
    ret = connect_num_of_domains_ret

class ConnectNumOfNetworks(ProcedureBase):
    id = 52
    name = 'connect_num_of_networks'
    args = None
    ret = connect_num_of_networks_ret

class DomainCoreDump(ProcedureBase):
    id = 53
    name = 'domain_core_dump'
    args = domain_core_dump_args
    ret = None

class DomainRestore(ProcedureBase):
    id = 54
    name = 'domain_restore'
    args = domain_restore_args
    ret = None

class DomainSave(ProcedureBase):
    id = 55
    name = 'domain_save'
    args = domain_save_args
    ret = None

class DomainGetSchedulerType(ProcedureBase):
    id = 56
    name = 'domain_get_scheduler_type'
    args = domain_get_scheduler_type_args
    ret = domain_get_scheduler_type_ret

class DomainGetSchedulerParameters(ProcedureBase):
    id = 57
    name = 'domain_get_scheduler_parameters'
    args = domain_get_scheduler_parameters_args
    ret = domain_get_scheduler_parameters_ret

class DomainSetSchedulerParameters(ProcedureBase):
    id = 58
    name = 'domain_set_scheduler_parameters'
    args = domain_set_scheduler_parameters_args
    ret = None

class ConnectGetHostname(ProcedureBase):
    id = 59
    name = 'connect_get_hostname'
    args = None
    ret = connect_get_hostname_ret

class ConnectSupportsFeature(ProcedureBase):
    id = 60
    name = 'connect_supports_feature'
    args = connect_supports_feature_args
    ret = connect_supports_feature_ret

class DomainMigratePrepare(ProcedureBase):
    id = 61
    name = 'domain_migrate_prepare'
    args = domain_migrate_prepare_args
    ret = domain_migrate_prepare_ret

class DomainMigratePerform(ProcedureBase):
    id = 62
    name = 'domain_migrate_perform'
    args = domain_migrate_perform_args
    ret = None

class DomainMigrateFinish(ProcedureBase):
    id = 63
    name = 'domain_migrate_finish'
    args = domain_migrate_finish_args
    ret = domain_migrate_finish_ret

class DomainBlockStats(ProcedureBase):
    id = 64
    name = 'domain_block_stats'
    args = domain_block_stats_args
    ret = domain_block_stats_ret

class DomainInterfaceStats(ProcedureBase):
    id = 65
    name = 'domain_interface_stats'
    args = domain_interface_stats_args
    ret = domain_interface_stats_ret

class AuthList(ProcedureBase):
    id = 66
    name = 'auth_list'
    args = None
    ret = auth_list_ret

class AuthSaslInit(ProcedureBase):
    id = 67
    name = 'auth_sasl_init'
    args = None
    ret = auth_sasl_init_ret

class AuthSaslStart(ProcedureBase):
    id = 68
    name = 'auth_sasl_start'
    args = auth_sasl_start_args
    ret = auth_sasl_start_ret

class AuthSaslStep(ProcedureBase):
    id = 69
    name = 'auth_sasl_step'
    args = auth_sasl_step_args
    ret = auth_sasl_step_ret

class AuthPolkit(ProcedureBase):
    id = 70
    name = 'auth_polkit'
    args = None
    ret = auth_polkit_ret

class ConnectNumOfStoragePools(ProcedureBase):
    id = 71
    name = 'connect_num_of_storage_pools'
    args = None
    ret = connect_num_of_storage_pools_ret

class ConnectListStoragePools(ProcedureBase):
    id = 72
    name = 'connect_list_storage_pools'
    args = connect_list_storage_pools_args
    ret = connect_list_storage_pools_ret

class ConnectNumOfDefinedStoragePools(ProcedureBase):
    id = 73
    name = 'connect_num_of_defined_storage_pools'
    args = None
    ret = connect_num_of_defined_storage_pools_ret

class ConnectListDefinedStoragePools(ProcedureBase):
    id = 74
    name = 'connect_list_defined_storage_pools'
    args = connect_list_defined_storage_pools_args
    ret = connect_list_defined_storage_pools_ret

class ConnectFindStoragePoolSources(ProcedureBase):
    id = 75
    name = 'connect_find_storage_pool_sources'
    args = connect_find_storage_pool_sources_args
    ret = connect_find_storage_pool_sources_ret

class StoragePoolCreateXml(ProcedureBase):
    id = 76
    name = 'storage_pool_create_xml'
    args = storage_pool_create_xml_args
    ret = storage_pool_create_xml_ret

class StoragePoolDefineXml(ProcedureBase):
    id = 77
    name = 'storage_pool_define_xml'
    args = storage_pool_define_xml_args
    ret = storage_pool_define_xml_ret

class StoragePoolCreate(ProcedureBase):
    id = 78
    name = 'storage_pool_create'
    args = storage_pool_create_args
    ret = None

class StoragePoolBuild(ProcedureBase):
    id = 79
    name = 'storage_pool_build'
    args = storage_pool_build_args
    ret = None

class StoragePoolDestroy(ProcedureBase):
    id = 80
    name = 'storage_pool_destroy'
    args = storage_pool_destroy_args
    ret = None

class StoragePoolDelete(ProcedureBase):
    id = 81
    name = 'storage_pool_delete'
    args = storage_pool_delete_args
    ret = None

class StoragePoolUndefine(ProcedureBase):
    id = 82
    name = 'storage_pool_undefine'
    args = storage_pool_undefine_args
    ret = None

class StoragePoolRefresh(ProcedureBase):
    id = 83
    name = 'storage_pool_refresh'
    args = storage_pool_refresh_args
    ret = None

class StoragePoolLookupByName(ProcedureBase):
    id = 84
    name = 'storage_pool_lookup_by_name'
    args = storage_pool_lookup_by_name_args
    ret = storage_pool_lookup_by_name_ret

class StoragePoolLookupByUuid(ProcedureBase):
    id = 85
    name = 'storage_pool_lookup_by_uuid'
    args = storage_pool_lookup_by_uuid_args
    ret = storage_pool_lookup_by_uuid_ret

class StoragePoolLookupByVolume(ProcedureBase):
    id = 86
    name = 'storage_pool_lookup_by_volume'
    args = storage_pool_lookup_by_volume_args
    ret = storage_pool_lookup_by_volume_ret

class StoragePoolGetInfo(ProcedureBase):
    id = 87
    name = 'storage_pool_get_info'
    args = storage_pool_get_info_args
    ret = storage_pool_get_info_ret

class StoragePoolGetXmlDesc(ProcedureBase):
    id = 88
    name = 'storage_pool_get_xml_desc'
    args = storage_pool_get_xml_desc_args
    ret = storage_pool_get_xml_desc_ret

class StoragePoolGetAutostart(ProcedureBase):
    id = 89
    name = 'storage_pool_get_autostart'
    args = storage_pool_get_autostart_args
    ret = storage_pool_get_autostart_ret

class StoragePoolSetAutostart(ProcedureBase):
    id = 90
    name = 'storage_pool_set_autostart'
    args = storage_pool_set_autostart_args
    ret = None

class StoragePoolNumOfVolumes(ProcedureBase):
    id = 91
    name = 'storage_pool_num_of_volumes'
    args = storage_pool_num_of_volumes_args
    ret = storage_pool_num_of_volumes_ret

class StoragePoolListVolumes(ProcedureBase):
    id = 92
    name = 'storage_pool_list_volumes'
    args = storage_pool_list_volumes_args
    ret = storage_pool_list_volumes_ret

class StorageVolCreateXml(ProcedureBase):
    id = 93
    name = 'storage_vol_create_xml'
    args = storage_vol_create_xml_args
    ret = storage_vol_create_xml_ret

class StorageVolDelete(ProcedureBase):
    id = 94
    name = 'storage_vol_delete'
    args = storage_vol_delete_args
    ret = None

class StorageVolLookupByName(ProcedureBase):
    id = 95
    name = 'storage_vol_lookup_by_name'
    args = storage_vol_lookup_by_name_args
    ret = storage_vol_lookup_by_name_ret

class StorageVolLookupByKey(ProcedureBase):
    id = 96
    name = 'storage_vol_lookup_by_key'
    args = storage_vol_lookup_by_key_args
    ret = storage_vol_lookup_by_key_ret

class StorageVolLookupByPath(ProcedureBase):
    id = 97
    name = 'storage_vol_lookup_by_path'
    args = storage_vol_lookup_by_path_args
    ret = storage_vol_lookup_by_path_ret

class StorageVolGetInfo(ProcedureBase):
    id = 98
    name = 'storage_vol_get_info'
    args = storage_vol_get_info_args
    ret = storage_vol_get_info_ret

class StorageVolGetXmlDesc(ProcedureBase):
    id = 99
    name = 'storage_vol_get_xml_desc'
    args = storage_vol_get_xml_desc_args
    ret = storage_vol_get_xml_desc_ret

class StorageVolGetPath(ProcedureBase):
    id = 100
    name = 'storage_vol_get_path'
    args = storage_vol_get_path_args
    ret = storage_vol_get_path_ret

class NodeGetCellsFreeMemory(ProcedureBase):
    id = 101
    name = 'node_get_cells_free_memory'
    args = node_get_cells_free_memory_args
    ret = node_get_cells_free_memory_ret

class NodeGetFreeMemory(ProcedureBase):
    id = 102
    name = 'node_get_free_memory'
    args = None
    ret = node_get_free_memory_ret

class DomainBlockPeek(ProcedureBase):
    id = 103
    name = 'domain_block_peek'
    args = domain_block_peek_args
    ret = domain_block_peek_ret

class DomainMemoryPeek(ProcedureBase):
    id = 104
    name = 'domain_memory_peek'
    args = domain_memory_peek_args
    ret = domain_memory_peek_ret

class ConnectDomainEventRegister(ProcedureBase):
    id = 105
    name = 'connect_domain_event_register'
    args = None
    ret = connect_domain_event_register_ret

class ConnectDomainEventDeregister(ProcedureBase):
    id = 106
    name = 'connect_domain_event_deregister'
    args = None
    ret = connect_domain_event_deregister_ret

class DomainEventLifecycle(ProcedureBase):
    id = 107
    name = 'domain_event_lifecycle'
    args = None
    ret = None

class DomainMigratePrepare2(ProcedureBase):
    id = 108
    name = 'domain_migrate_prepare2'
    args = domain_migrate_prepare2_args
    ret = domain_migrate_prepare2_ret

class DomainMigrateFinish2(ProcedureBase):
    id = 109
    name = 'domain_migrate_finish2'
    args = domain_migrate_finish2_args
    ret = domain_migrate_finish2_ret

class ConnectGetUri(ProcedureBase):
    id = 110
    name = 'connect_get_uri'
    args = None
    ret = connect_get_uri_ret

class NodeNumOfDevices(ProcedureBase):
    id = 111
    name = 'node_num_of_devices'
    args = node_num_of_devices_args
    ret = node_num_of_devices_ret

class NodeListDevices(ProcedureBase):
    id = 112
    name = 'node_list_devices'
    args = node_list_devices_args
    ret = node_list_devices_ret

class NodeDeviceLookupByName(ProcedureBase):
    id = 113
    name = 'node_device_lookup_by_name'
    args = node_device_lookup_by_name_args
    ret = node_device_lookup_by_name_ret

class NodeDeviceGetXmlDesc(ProcedureBase):
    id = 114
    name = 'node_device_get_xml_desc'
    args = node_device_get_xml_desc_args
    ret = node_device_get_xml_desc_ret

class NodeDeviceGetParent(ProcedureBase):
    id = 115
    name = 'node_device_get_parent'
    args = node_device_get_parent_args
    ret = node_device_get_parent_ret

class NodeDeviceNumOfCaps(ProcedureBase):
    id = 116
    name = 'node_device_num_of_caps'
    args = node_device_num_of_caps_args
    ret = node_device_num_of_caps_ret

class NodeDeviceListCaps(ProcedureBase):
    id = 117
    name = 'node_device_list_caps'
    args = node_device_list_caps_args
    ret = node_device_list_caps_ret

class NodeDeviceDettach(ProcedureBase):
    id = 118
    name = 'node_device_dettach'
    args = node_device_dettach_args
    ret = None

class NodeDeviceReAttach(ProcedureBase):
    id = 119
    name = 'node_device_re_attach'
    args = node_device_re_attach_args
    ret = None

class NodeDeviceReset(ProcedureBase):
    id = 120
    name = 'node_device_reset'
    args = node_device_reset_args
    ret = None

class DomainGetSecurityLabel(ProcedureBase):
    id = 121
    name = 'domain_get_security_label'
    args = domain_get_security_label_args
    ret = domain_get_security_label_ret

class NodeGetSecurityModel(ProcedureBase):
    id = 122
    name = 'node_get_security_model'
    args = None
    ret = node_get_security_model_ret

class NodeDeviceCreateXml(ProcedureBase):
    id = 123
    name = 'node_device_create_xml'
    args = node_device_create_xml_args
    ret = node_device_create_xml_ret

class NodeDeviceDestroy(ProcedureBase):
    id = 124
    name = 'node_device_destroy'
    args = node_device_destroy_args
    ret = None

class StorageVolCreateXmlFrom(ProcedureBase):
    id = 125
    name = 'storage_vol_create_xml_from'
    args = storage_vol_create_xml_from_args
    ret = storage_vol_create_xml_from_ret

class ConnectNumOfInterfaces(ProcedureBase):
    id = 126
    name = 'connect_num_of_interfaces'
    args = None
    ret = connect_num_of_interfaces_ret

class ConnectListInterfaces(ProcedureBase):
    id = 127
    name = 'connect_list_interfaces'
    args = connect_list_interfaces_args
    ret = connect_list_interfaces_ret

class InterfaceLookupByName(ProcedureBase):
    id = 128
    name = 'interface_lookup_by_name'
    args = interface_lookup_by_name_args
    ret = interface_lookup_by_name_ret

class InterfaceLookupByMacString(ProcedureBase):
    id = 129
    name = 'interface_lookup_by_mac_string'
    args = interface_lookup_by_mac_string_args
    ret = interface_lookup_by_mac_string_ret

class InterfaceGetXmlDesc(ProcedureBase):
    id = 130
    name = 'interface_get_xml_desc'
    args = interface_get_xml_desc_args
    ret = interface_get_xml_desc_ret

class InterfaceDefineXml(ProcedureBase):
    id = 131
    name = 'interface_define_xml'
    args = interface_define_xml_args
    ret = interface_define_xml_ret

class InterfaceUndefine(ProcedureBase):
    id = 132
    name = 'interface_undefine'
    args = interface_undefine_args
    ret = None

class InterfaceCreate(ProcedureBase):
    id = 133
    name = 'interface_create'
    args = interface_create_args
    ret = None

class InterfaceDestroy(ProcedureBase):
    id = 134
    name = 'interface_destroy'
    args = interface_destroy_args
    ret = None

class ConnectDomainXmlFromNative(ProcedureBase):
    id = 135
    name = 'connect_domain_xml_from_native'
    args = connect_domain_xml_from_native_args
    ret = connect_domain_xml_from_native_ret

class ConnectDomainXmlToNative(ProcedureBase):
    id = 136
    name = 'connect_domain_xml_to_native'
    args = connect_domain_xml_to_native_args
    ret = connect_domain_xml_to_native_ret

class ConnectNumOfDefinedInterfaces(ProcedureBase):
    id = 137
    name = 'connect_num_of_defined_interfaces'
    args = None
    ret = connect_num_of_defined_interfaces_ret

class ConnectListDefinedInterfaces(ProcedureBase):
    id = 138
    name = 'connect_list_defined_interfaces'
    args = connect_list_defined_interfaces_args
    ret = connect_list_defined_interfaces_ret

class ConnectNumOfSecrets(ProcedureBase):
    id = 139
    name = 'connect_num_of_secrets'
    args = None
    ret = connect_num_of_secrets_ret

class ConnectListSecrets(ProcedureBase):
    id = 140
    name = 'connect_list_secrets'
    args = connect_list_secrets_args
    ret = connect_list_secrets_ret

class SecretLookupByUuid(ProcedureBase):
    id = 141
    name = 'secret_lookup_by_uuid'
    args = secret_lookup_by_uuid_args
    ret = secret_lookup_by_uuid_ret

class SecretDefineXml(ProcedureBase):
    id = 142
    name = 'secret_define_xml'
    args = secret_define_xml_args
    ret = secret_define_xml_ret

class SecretGetXmlDesc(ProcedureBase):
    id = 143
    name = 'secret_get_xml_desc'
    args = secret_get_xml_desc_args
    ret = secret_get_xml_desc_ret

class SecretSetValue(ProcedureBase):
    id = 144
    name = 'secret_set_value'
    args = secret_set_value_args
    ret = None

class SecretGetValue(ProcedureBase):
    id = 145
    name = 'secret_get_value'
    args = secret_get_value_args
    ret = secret_get_value_ret

class SecretUndefine(ProcedureBase):
    id = 146
    name = 'secret_undefine'
    args = secret_undefine_args
    ret = None

class SecretLookupByUsage(ProcedureBase):
    id = 147
    name = 'secret_lookup_by_usage'
    args = secret_lookup_by_usage_args
    ret = secret_lookup_by_usage_ret

class DomainMigratePrepareTunnel(ProcedureBase):
    id = 148
    name = 'domain_migrate_prepare_tunnel'
    args = domain_migrate_prepare_tunnel_args
    ret = None

class ConnectIsSecure(ProcedureBase):
    id = 149
    name = 'connect_is_secure'
    args = None
    ret = connect_is_secure_ret

class DomainIsActive(ProcedureBase):
    id = 150
    name = 'domain_is_active'
    args = domain_is_active_args
    ret = domain_is_active_ret

class DomainIsPersistent(ProcedureBase):
    id = 151
    name = 'domain_is_persistent'
    args = domain_is_persistent_args
    ret = domain_is_persistent_ret

class NetworkIsActive(ProcedureBase):
    id = 152
    name = 'network_is_active'
    args = network_is_active_args
    ret = network_is_active_ret

class NetworkIsPersistent(ProcedureBase):
    id = 153
    name = 'network_is_persistent'
    args = network_is_persistent_args
    ret = network_is_persistent_ret

class StoragePoolIsActive(ProcedureBase):
    id = 154
    name = 'storage_pool_is_active'
    args = storage_pool_is_active_args
    ret = storage_pool_is_active_ret

class StoragePoolIsPersistent(ProcedureBase):
    id = 155
    name = 'storage_pool_is_persistent'
    args = storage_pool_is_persistent_args
    ret = storage_pool_is_persistent_ret

class InterfaceIsActive(ProcedureBase):
    id = 156
    name = 'interface_is_active'
    args = interface_is_active_args
    ret = interface_is_active_ret

class ConnectGetLibVersion(ProcedureBase):
    id = 157
    name = 'connect_get_lib_version'
    args = None
    ret = connect_get_lib_version_ret

class ConnectCompareCpu(ProcedureBase):
    id = 158
    name = 'connect_compare_cpu'
    args = connect_compare_cpu_args
    ret = connect_compare_cpu_ret

class DomainMemoryStats(ProcedureBase):
    id = 159
    name = 'domain_memory_stats'
    args = domain_memory_stats_args
    ret = domain_memory_stats_ret

class DomainAttachDeviceFlags(ProcedureBase):
    id = 160
    name = 'domain_attach_device_flags'
    args = domain_attach_device_flags_args
    ret = None

class DomainDetachDeviceFlags(ProcedureBase):
    id = 161
    name = 'domain_detach_device_flags'
    args = domain_detach_device_flags_args
    ret = None

class ConnectBaselineCpu(ProcedureBase):
    id = 162
    name = 'connect_baseline_cpu'
    args = connect_baseline_cpu_args
    ret = connect_baseline_cpu_ret

class DomainGetJobInfo(ProcedureBase):
    id = 163
    name = 'domain_get_job_info'
    args = domain_get_job_info_args
    ret = domain_get_job_info_ret

class DomainAbortJob(ProcedureBase):
    id = 164
    name = 'domain_abort_job'
    args = domain_abort_job_args
    ret = None

class StorageVolWipe(ProcedureBase):
    id = 165
    name = 'storage_vol_wipe'
    args = storage_vol_wipe_args
    ret = None

class DomainMigrateSetMaxDowntime(ProcedureBase):
    id = 166
    name = 'domain_migrate_set_max_downtime'
    args = domain_migrate_set_max_downtime_args
    ret = None

class ConnectDomainEventRegisterAny(ProcedureBase):
    id = 167
    name = 'connect_domain_event_register_any'
    args = connect_domain_event_register_any_args
    ret = None

class ConnectDomainEventDeregisterAny(ProcedureBase):
    id = 168
    name = 'connect_domain_event_deregister_any'
    args = connect_domain_event_deregister_any_args
    ret = None

class DomainEventReboot(ProcedureBase):
    id = 169
    name = 'domain_event_reboot'
    args = None
    ret = None

class DomainEventRtcChange(ProcedureBase):
    id = 170
    name = 'domain_event_rtc_change'
    args = None
    ret = None

class DomainEventWatchdog(ProcedureBase):
    id = 171
    name = 'domain_event_watchdog'
    args = None
    ret = None

class DomainEventIoError(ProcedureBase):
    id = 172
    name = 'domain_event_io_error'
    args = None
    ret = None

class DomainEventGraphics(ProcedureBase):
    id = 173
    name = 'domain_event_graphics'
    args = None
    ret = None

class DomainUpdateDeviceFlags(ProcedureBase):
    id = 174
    name = 'domain_update_device_flags'
    args = domain_update_device_flags_args
    ret = None

class NwfilterLookupByName(ProcedureBase):
    id = 175
    name = 'nwfilter_lookup_by_name'
    args = nwfilter_lookup_by_name_args
    ret = nwfilter_lookup_by_name_ret

class NwfilterLookupByUuid(ProcedureBase):
    id = 176
    name = 'nwfilter_lookup_by_uuid'
    args = nwfilter_lookup_by_uuid_args
    ret = nwfilter_lookup_by_uuid_ret

class NwfilterGetXmlDesc(ProcedureBase):
    id = 177
    name = 'nwfilter_get_xml_desc'
    args = nwfilter_get_xml_desc_args
    ret = nwfilter_get_xml_desc_ret

class ConnectNumOfNwfilters(ProcedureBase):
    id = 178
    name = 'connect_num_of_nwfilters'
    args = None
    ret = connect_num_of_nwfilters_ret

class ConnectListNwfilters(ProcedureBase):
    id = 179
    name = 'connect_list_nwfilters'
    args = connect_list_nwfilters_args
    ret = connect_list_nwfilters_ret

class NwfilterDefineXml(ProcedureBase):
    id = 180
    name = 'nwfilter_define_xml'
    args = nwfilter_define_xml_args
    ret = nwfilter_define_xml_ret

class NwfilterUndefine(ProcedureBase):
    id = 181
    name = 'nwfilter_undefine'
    args = nwfilter_undefine_args
    ret = None

class DomainManagedSave(ProcedureBase):
    id = 182
    name = 'domain_managed_save'
    args = domain_managed_save_args
    ret = None

class DomainHasManagedSaveImage(ProcedureBase):
    id = 183
    name = 'domain_has_managed_save_image'
    args = domain_has_managed_save_image_args
    ret = domain_has_managed_save_image_ret

class DomainManagedSaveRemove(ProcedureBase):
    id = 184
    name = 'domain_managed_save_remove'
    args = domain_managed_save_remove_args
    ret = None

class DomainSnapshotCreateXml(ProcedureBase):
    id = 185
    name = 'domain_snapshot_create_xml'
    args = domain_snapshot_create_xml_args
    ret = domain_snapshot_create_xml_ret

class DomainSnapshotGetXmlDesc(ProcedureBase):
    id = 186
    name = 'domain_snapshot_get_xml_desc'
    args = domain_snapshot_get_xml_desc_args
    ret = domain_snapshot_get_xml_desc_ret

class DomainSnapshotNum(ProcedureBase):
    id = 187
    name = 'domain_snapshot_num'
    args = domain_snapshot_num_args
    ret = domain_snapshot_num_ret

class DomainSnapshotListNames(ProcedureBase):
    id = 188
    name = 'domain_snapshot_list_names'
    args = domain_snapshot_list_names_args
    ret = domain_snapshot_list_names_ret

class DomainSnapshotLookupByName(ProcedureBase):
    id = 189
    name = 'domain_snapshot_lookup_by_name'
    args = domain_snapshot_lookup_by_name_args
    ret = domain_snapshot_lookup_by_name_ret

class DomainHasCurrentSnapshot(ProcedureBase):
    id = 190
    name = 'domain_has_current_snapshot'
    args = domain_has_current_snapshot_args
    ret = domain_has_current_snapshot_ret

class DomainSnapshotCurrent(ProcedureBase):
    id = 191
    name = 'domain_snapshot_current'
    args = domain_snapshot_current_args
    ret = domain_snapshot_current_ret

class DomainRevertToSnapshot(ProcedureBase):
    id = 192
    name = 'domain_revert_to_snapshot'
    args = domain_revert_to_snapshot_args
    ret = None

class DomainSnapshotDelete(ProcedureBase):
    id = 193
    name = 'domain_snapshot_delete'
    args = domain_snapshot_delete_args
    ret = None

class DomainGetBlockInfo(ProcedureBase):
    id = 194
    name = 'domain_get_block_info'
    args = domain_get_block_info_args
    ret = domain_get_block_info_ret

class DomainEventIoErrorReason(ProcedureBase):
    id = 195
    name = 'domain_event_io_error_reason'
    args = None
    ret = None

class DomainCreateWithFlags(ProcedureBase):
    id = 196
    name = 'domain_create_with_flags'
    args = domain_create_with_flags_args
    ret = domain_create_with_flags_ret

class DomainSetMemoryParameters(ProcedureBase):
    id = 197
    name = 'domain_set_memory_parameters'
    args = domain_set_memory_parameters_args
    ret = None

class DomainGetMemoryParameters(ProcedureBase):
    id = 198
    name = 'domain_get_memory_parameters'
    args = domain_get_memory_parameters_args
    ret = domain_get_memory_parameters_ret

class DomainSetVcpusFlags(ProcedureBase):
    id = 199
    name = 'domain_set_vcpus_flags'
    args = domain_set_vcpus_flags_args
    ret = None

class DomainGetVcpusFlags(ProcedureBase):
    id = 200
    name = 'domain_get_vcpus_flags'
    args = domain_get_vcpus_flags_args
    ret = domain_get_vcpus_flags_ret

class DomainOpenConsole(ProcedureBase):
    id = 201
    name = 'domain_open_console'
    args = domain_open_console_args
    ret = None

class DomainIsUpdated(ProcedureBase):
    id = 202
    name = 'domain_is_updated'
    args = domain_is_updated_args
    ret = domain_is_updated_ret

class ConnectGetSysinfo(ProcedureBase):
    id = 203
    name = 'connect_get_sysinfo'
    args = connect_get_sysinfo_args
    ret = connect_get_sysinfo_ret

class DomainSetMemoryFlags(ProcedureBase):
    id = 204
    name = 'domain_set_memory_flags'
    args = domain_set_memory_flags_args
    ret = None

class DomainSetBlkioParameters(ProcedureBase):
    id = 205
    name = 'domain_set_blkio_parameters'
    args = domain_set_blkio_parameters_args
    ret = None

class DomainGetBlkioParameters(ProcedureBase):
    id = 206
    name = 'domain_get_blkio_parameters'
    args = domain_get_blkio_parameters_args
    ret = domain_get_blkio_parameters_ret

class DomainMigrateSetMaxSpeed(ProcedureBase):
    id = 207
    name = 'domain_migrate_set_max_speed'
    args = domain_migrate_set_max_speed_args
    ret = None

class StorageVolUpload(ProcedureBase):
    id = 208
    name = 'storage_vol_upload'
    args = storage_vol_upload_args
    ret = None

class StorageVolDownload(ProcedureBase):
    id = 209
    name = 'storage_vol_download'
    args = storage_vol_download_args
    ret = None

class DomainInjectNmi(ProcedureBase):
    id = 210
    name = 'domain_inject_nmi'
    args = domain_inject_nmi_args
    ret = None

class DomainScreenshot(ProcedureBase):
    id = 211
    name = 'domain_screenshot'
    args = domain_screenshot_args
    ret = domain_screenshot_ret

class DomainGetState(ProcedureBase):
    id = 212
    name = 'domain_get_state'
    args = domain_get_state_args
    ret = domain_get_state_ret

class DomainMigrateBegin3(ProcedureBase):
    id = 213
    name = 'domain_migrate_begin3'
    args = domain_migrate_begin3_args
    ret = domain_migrate_begin3_ret

class DomainMigratePrepare3(ProcedureBase):
    id = 214
    name = 'domain_migrate_prepare3'
    args = domain_migrate_prepare3_args
    ret = domain_migrate_prepare3_ret

class DomainMigratePrepareTunnel3(ProcedureBase):
    id = 215
    name = 'domain_migrate_prepare_tunnel3'
    args = domain_migrate_prepare_tunnel3_args
    ret = domain_migrate_prepare_tunnel3_ret

class DomainMigratePerform3(ProcedureBase):
    id = 216
    name = 'domain_migrate_perform3'
    args = domain_migrate_perform3_args
    ret = domain_migrate_perform3_ret

class DomainMigrateFinish3(ProcedureBase):
    id = 217
    name = 'domain_migrate_finish3'
    args = domain_migrate_finish3_args
    ret = domain_migrate_finish3_ret

class DomainMigrateConfirm3(ProcedureBase):
    id = 218
    name = 'domain_migrate_confirm3'
    args = domain_migrate_confirm3_args
    ret = None

class DomainSetSchedulerParametersFlags(ProcedureBase):
    id = 219
    name = 'domain_set_scheduler_parameters_flags'
    args = domain_set_scheduler_parameters_flags_args
    ret = None

class InterfaceChangeBegin(ProcedureBase):
    id = 220
    name = 'interface_change_begin'
    args = interface_change_begin_args
    ret = None

class InterfaceChangeCommit(ProcedureBase):
    id = 221
    name = 'interface_change_commit'
    args = interface_change_commit_args
    ret = None

class InterfaceChangeRollback(ProcedureBase):
    id = 222
    name = 'interface_change_rollback'
    args = interface_change_rollback_args
    ret = None

class DomainGetSchedulerParametersFlags(ProcedureBase):
    id = 223
    name = 'domain_get_scheduler_parameters_flags'
    args = domain_get_scheduler_parameters_flags_args
    ret = domain_get_scheduler_parameters_flags_ret

class DomainEventControlError(ProcedureBase):
    id = 224
    name = 'domain_event_control_error'
    args = None
    ret = None

class DomainPinVcpuFlags(ProcedureBase):
    id = 225
    name = 'domain_pin_vcpu_flags'
    args = domain_pin_vcpu_flags_args
    ret = None

class DomainSendKey(ProcedureBase):
    id = 226
    name = 'domain_send_key'
    args = domain_send_key_args
    ret = None

class NodeGetCpuStats(ProcedureBase):
    id = 227
    name = 'node_get_cpu_stats'
    args = node_get_cpu_stats_args
    ret = node_get_cpu_stats_ret

class NodeGetMemoryStats(ProcedureBase):
    id = 228
    name = 'node_get_memory_stats'
    args = node_get_memory_stats_args
    ret = node_get_memory_stats_ret

class DomainGetControlInfo(ProcedureBase):
    id = 229
    name = 'domain_get_control_info'
    args = domain_get_control_info_args
    ret = domain_get_control_info_ret

class DomainGetVcpuPinInfo(ProcedureBase):
    id = 230
    name = 'domain_get_vcpu_pin_info'
    args = domain_get_vcpu_pin_info_args
    ret = domain_get_vcpu_pin_info_ret

class DomainUndefineFlags(ProcedureBase):
    id = 231
    name = 'domain_undefine_flags'
    args = domain_undefine_flags_args
    ret = None

class DomainSaveFlags(ProcedureBase):
    id = 232
    name = 'domain_save_flags'
    args = domain_save_flags_args
    ret = None

class DomainRestoreFlags(ProcedureBase):
    id = 233
    name = 'domain_restore_flags'
    args = domain_restore_flags_args
    ret = None

class DomainDestroyFlags(ProcedureBase):
    id = 234
    name = 'domain_destroy_flags'
    args = domain_destroy_flags_args
    ret = None

class DomainSaveImageGetXmlDesc(ProcedureBase):
    id = 235
    name = 'domain_save_image_get_xml_desc'
    args = domain_save_image_get_xml_desc_args
    ret = domain_save_image_get_xml_desc_ret

class DomainSaveImageDefineXml(ProcedureBase):
    id = 236
    name = 'domain_save_image_define_xml'
    args = domain_save_image_define_xml_args
    ret = None

class DomainBlockJobAbort(ProcedureBase):
    id = 237
    name = 'domain_block_job_abort'
    args = domain_block_job_abort_args
    ret = None

class DomainGetBlockJobInfo(ProcedureBase):
    id = 238
    name = 'domain_get_block_job_info'
    args = domain_get_block_job_info_args
    ret = domain_get_block_job_info_ret

class DomainBlockJobSetSpeed(ProcedureBase):
    id = 239
    name = 'domain_block_job_set_speed'
    args = domain_block_job_set_speed_args
    ret = None

class DomainBlockPull(ProcedureBase):
    id = 240
    name = 'domain_block_pull'
    args = domain_block_pull_args
    ret = None

class DomainEventBlockJob(ProcedureBase):
    id = 241
    name = 'domain_event_block_job'
    args = None
    ret = None

class DomainMigrateGetMaxSpeed(ProcedureBase):
    id = 242
    name = 'domain_migrate_get_max_speed'
    args = domain_migrate_get_max_speed_args
    ret = domain_migrate_get_max_speed_ret

class DomainBlockStatsFlags(ProcedureBase):
    id = 243
    name = 'domain_block_stats_flags'
    args = domain_block_stats_flags_args
    ret = domain_block_stats_flags_ret

class DomainSnapshotGetParent(ProcedureBase):
    id = 244
    name = 'domain_snapshot_get_parent'
    args = domain_snapshot_get_parent_args
    ret = domain_snapshot_get_parent_ret

class DomainReset(ProcedureBase):
    id = 245
    name = 'domain_reset'
    args = domain_reset_args
    ret = None

class DomainSnapshotNumChildren(ProcedureBase):
    id = 246
    name = 'domain_snapshot_num_children'
    args = domain_snapshot_num_children_args
    ret = domain_snapshot_num_children_ret

class DomainSnapshotListChildrenNames(ProcedureBase):
    id = 247
    name = 'domain_snapshot_list_children_names'
    args = domain_snapshot_list_children_names_args
    ret = domain_snapshot_list_children_names_ret

class DomainEventDiskChange(ProcedureBase):
    id = 248
    name = 'domain_event_disk_change'
    args = None
    ret = None

class DomainOpenGraphics(ProcedureBase):
    id = 249
    name = 'domain_open_graphics'
    args = domain_open_graphics_args
    ret = None

class NodeSuspendForDuration(ProcedureBase):
    id = 250
    name = 'node_suspend_for_duration'
    args = node_suspend_for_duration_args
    ret = None

class DomainBlockResize(ProcedureBase):
    id = 251
    name = 'domain_block_resize'
    args = domain_block_resize_args
    ret = None

class DomainSetBlockIoTune(ProcedureBase):
    id = 252
    name = 'domain_set_block_io_tune'
    args = domain_set_block_io_tune_args
    ret = None

class DomainGetBlockIoTune(ProcedureBase):
    id = 253
    name = 'domain_get_block_io_tune'
    args = domain_get_block_io_tune_args
    ret = domain_get_block_io_tune_ret

class DomainSetNumaParameters(ProcedureBase):
    id = 254
    name = 'domain_set_numa_parameters'
    args = domain_set_numa_parameters_args
    ret = None

class DomainGetNumaParameters(ProcedureBase):
    id = 255
    name = 'domain_get_numa_parameters'
    args = domain_get_numa_parameters_args
    ret = domain_get_numa_parameters_ret

class DomainSetInterfaceParameters(ProcedureBase):
    id = 256
    name = 'domain_set_interface_parameters'
    args = domain_set_interface_parameters_args
    ret = None

class DomainGetInterfaceParameters(ProcedureBase):
    id = 257
    name = 'domain_get_interface_parameters'
    args = domain_get_interface_parameters_args
    ret = domain_get_interface_parameters_ret

class DomainShutdownFlags(ProcedureBase):
    id = 258
    name = 'domain_shutdown_flags'
    args = domain_shutdown_flags_args
    ret = None

class StorageVolWipePattern(ProcedureBase):
    id = 259
    name = 'storage_vol_wipe_pattern'
    args = storage_vol_wipe_pattern_args
    ret = None

class StorageVolResize(ProcedureBase):
    id = 260
    name = 'storage_vol_resize'
    args = storage_vol_resize_args
    ret = None

class DomainPmSuspendForDuration(ProcedureBase):
    id = 261
    name = 'domain_pm_suspend_for_duration'
    args = domain_pm_suspend_for_duration_args
    ret = None

class DomainGetCpuStats(ProcedureBase):
    id = 262
    name = 'domain_get_cpu_stats'
    args = domain_get_cpu_stats_args
    ret = domain_get_cpu_stats_ret

class DomainGetDiskErrors(ProcedureBase):
    id = 263
    name = 'domain_get_disk_errors'
    args = domain_get_disk_errors_args
    ret = domain_get_disk_errors_ret

class DomainSetMetadata(ProcedureBase):
    id = 264
    name = 'domain_set_metadata'
    args = domain_set_metadata_args
    ret = None

class DomainGetMetadata(ProcedureBase):
    id = 265
    name = 'domain_get_metadata'
    args = domain_get_metadata_args
    ret = domain_get_metadata_ret

class DomainBlockRebase(ProcedureBase):
    id = 266
    name = 'domain_block_rebase'
    args = domain_block_rebase_args
    ret = None

class DomainPmWakeup(ProcedureBase):
    id = 267
    name = 'domain_pm_wakeup'
    args = domain_pm_wakeup_args
    ret = None

class DomainEventTrayChange(ProcedureBase):
    id = 268
    name = 'domain_event_tray_change'
    args = None
    ret = None

class DomainEventPmwakeup(ProcedureBase):
    id = 269
    name = 'domain_event_pmwakeup'
    args = None
    ret = None

class DomainEventPmsuspend(ProcedureBase):
    id = 270
    name = 'domain_event_pmsuspend'
    args = None
    ret = None

class DomainSnapshotIsCurrent(ProcedureBase):
    id = 271
    name = 'domain_snapshot_is_current'
    args = domain_snapshot_is_current_args
    ret = domain_snapshot_is_current_ret

class DomainSnapshotHasMetadata(ProcedureBase):
    id = 272
    name = 'domain_snapshot_has_metadata'
    args = domain_snapshot_has_metadata_args
    ret = domain_snapshot_has_metadata_ret

class ConnectListAllDomains(ProcedureBase):
    id = 273
    name = 'connect_list_all_domains'
    args = connect_list_all_domains_args
    ret = connect_list_all_domains_ret

class DomainListAllSnapshots(ProcedureBase):
    id = 274
    name = 'domain_list_all_snapshots'
    args = domain_list_all_snapshots_args
    ret = domain_list_all_snapshots_ret

class DomainSnapshotListAllChildren(ProcedureBase):
    id = 275
    name = 'domain_snapshot_list_all_children'
    args = domain_snapshot_list_all_children_args
    ret = domain_snapshot_list_all_children_ret

class DomainEventBalloonChange(ProcedureBase):
    id = 276
    name = 'domain_event_balloon_change'
    args = None
    ret = None

class DomainGetHostname(ProcedureBase):
    id = 277
    name = 'domain_get_hostname'
    args = domain_get_hostname_args
    ret = domain_get_hostname_ret

class DomainGetSecurityLabelList(ProcedureBase):
    id = 278
    name = 'domain_get_security_label_list'
    args = domain_get_security_label_list_args
    ret = domain_get_security_label_list_ret

class DomainPinEmulator(ProcedureBase):
    id = 279
    name = 'domain_pin_emulator'
    args = domain_pin_emulator_args
    ret = None

class DomainGetEmulatorPinInfo(ProcedureBase):
    id = 280
    name = 'domain_get_emulator_pin_info'
    args = domain_get_emulator_pin_info_args
    ret = domain_get_emulator_pin_info_ret

class ConnectListAllStoragePools(ProcedureBase):
    id = 281
    name = 'connect_list_all_storage_pools'
    args = connect_list_all_storage_pools_args
    ret = connect_list_all_storage_pools_ret

class StoragePoolListAllVolumes(ProcedureBase):
    id = 282
    name = 'storage_pool_list_all_volumes'
    args = storage_pool_list_all_volumes_args
    ret = storage_pool_list_all_volumes_ret

class ConnectListAllNetworks(ProcedureBase):
    id = 283
    name = 'connect_list_all_networks'
    args = connect_list_all_networks_args
    ret = connect_list_all_networks_ret

class ConnectListAllInterfaces(ProcedureBase):
    id = 284
    name = 'connect_list_all_interfaces'
    args = connect_list_all_interfaces_args
    ret = connect_list_all_interfaces_ret

class ConnectListAllNodeDevices(ProcedureBase):
    id = 285
    name = 'connect_list_all_node_devices'
    args = connect_list_all_node_devices_args
    ret = connect_list_all_node_devices_ret

class ConnectListAllNwfilters(ProcedureBase):
    id = 286
    name = 'connect_list_all_nwfilters'
    args = connect_list_all_nwfilters_args
    ret = connect_list_all_nwfilters_ret

class ConnectListAllSecrets(ProcedureBase):
    id = 287
    name = 'connect_list_all_secrets'
    args = connect_list_all_secrets_args
    ret = connect_list_all_secrets_ret

class NodeSetMemoryParameters(ProcedureBase):
    id = 288
    name = 'node_set_memory_parameters'
    args = node_set_memory_parameters_args
    ret = None

class NodeGetMemoryParameters(ProcedureBase):
    id = 289
    name = 'node_get_memory_parameters'
    args = node_get_memory_parameters_args
    ret = node_get_memory_parameters_ret

class DomainBlockCommit(ProcedureBase):
    id = 290
    name = 'domain_block_commit'
    args = domain_block_commit_args
    ret = None

class NetworkUpdate(ProcedureBase):
    id = 291
    name = 'network_update'
    args = network_update_args
    ret = None

class DomainEventPmsuspendDisk(ProcedureBase):
    id = 292
    name = 'domain_event_pmsuspend_disk'
    args = None
    ret = None

class NodeGetCpuMap(ProcedureBase):
    id = 293
    name = 'node_get_cpu_map'
    args = node_get_cpu_map_args
    ret = node_get_cpu_map_ret

class DomainFstrim(ProcedureBase):
    id = 294
    name = 'domain_fstrim'
    args = domain_fstrim_args
    ret = None

class DomainSendProcessSignal(ProcedureBase):
    id = 295
    name = 'domain_send_process_signal'
    args = domain_send_process_signal_args
    ret = None

class DomainOpenChannel(ProcedureBase):
    id = 296
    name = 'domain_open_channel'
    args = domain_open_channel_args
    ret = None

class NodeDeviceLookupScsiHostByWwn(ProcedureBase):
    id = 297
    name = 'node_device_lookup_scsi_host_by_wwn'
    args = node_device_lookup_scsi_host_by_wwn_args
    ret = node_device_lookup_scsi_host_by_wwn_ret

class DomainGetJobStats(ProcedureBase):
    id = 298
    name = 'domain_get_job_stats'
    args = domain_get_job_stats_args
    ret = domain_get_job_stats_ret

class DomainMigrateGetCompressionCache(ProcedureBase):
    id = 299
    name = 'domain_migrate_get_compression_cache'
    args = domain_migrate_get_compression_cache_args
    ret = domain_migrate_get_compression_cache_ret

class DomainMigrateSetCompressionCache(ProcedureBase):
    id = 300
    name = 'domain_migrate_set_compression_cache'
    args = domain_migrate_set_compression_cache_args
    ret = None

class NodeDeviceDetachFlags(ProcedureBase):
    id = 301
    name = 'node_device_detach_flags'
    args = node_device_detach_flags_args
    ret = None

class DomainMigrateBegin3Params(ProcedureBase):
    id = 302
    name = 'domain_migrate_begin3_params'
    args = domain_migrate_begin3_params_args
    ret = domain_migrate_begin3_params_ret

class DomainMigratePrepare3Params(ProcedureBase):
    id = 303
    name = 'domain_migrate_prepare3_params'
    args = domain_migrate_prepare3_params_args
    ret = domain_migrate_prepare3_params_ret

class DomainMigratePrepareTunnel3Params(ProcedureBase):
    id = 304
    name = 'domain_migrate_prepare_tunnel3_params'
    args = domain_migrate_prepare_tunnel3_params_args
    ret = domain_migrate_prepare_tunnel3_params_ret

class DomainMigratePerform3Params(ProcedureBase):
    id = 305
    name = 'domain_migrate_perform3_params'
    args = domain_migrate_perform3_params_args
    ret = domain_migrate_perform3_params_ret

class DomainMigrateFinish3Params(ProcedureBase):
    id = 306
    name = 'domain_migrate_finish3_params'
    args = domain_migrate_finish3_params_args
    ret = domain_migrate_finish3_params_ret

class DomainMigrateConfirm3Params(ProcedureBase):
    id = 307
    name = 'domain_migrate_confirm3_params'
    args = domain_migrate_confirm3_params_args
    ret = None

class DomainSetMemoryStatsPeriod(ProcedureBase):
    id = 308
    name = 'domain_set_memory_stats_period'
    args = domain_set_memory_stats_period_args
    ret = None

class DomainCreateXmlWithFiles(ProcedureBase):
    id = 309
    name = 'domain_create_xml_with_files'
    args = domain_create_xml_with_files_args
    ret = domain_create_xml_with_files_ret

class DomainCreateWithFiles(ProcedureBase):
    id = 310
    name = 'domain_create_with_files'
    args = domain_create_with_files_args
    ret = domain_create_with_files_ret

class DomainEventDeviceRemoved(ProcedureBase):
    id = 311
    name = 'domain_event_device_removed'
    args = None
    ret = None

class ConnectGetCpuModelNames(ProcedureBase):
    id = 312
    name = 'connect_get_cpu_model_names'
    args = connect_get_cpu_model_names_args
    ret = connect_get_cpu_model_names_ret

PROCEDURE_BY_NAME = {
    'connect_open': ConnectOpen,
    'connect_close': ConnectClose,
    'connect_get_type': ConnectGetType,
    'connect_get_version': ConnectGetVersion,
    'connect_get_max_vcpus': ConnectGetMaxVcpus,
    'node_get_info': NodeGetInfo,
    'connect_get_capabilities': ConnectGetCapabilities,
    'domain_attach_device': DomainAttachDevice,
    'domain_create': DomainCreate,
    'domain_create_xml': DomainCreateXml,
    'domain_define_xml': DomainDefineXml,
    'domain_destroy': DomainDestroy,
    'domain_detach_device': DomainDetachDevice,
    'domain_get_xml_desc': DomainGetXmlDesc,
    'domain_get_autostart': DomainGetAutostart,
    'domain_get_info': DomainGetInfo,
    'domain_get_max_memory': DomainGetMaxMemory,
    'domain_get_max_vcpus': DomainGetMaxVcpus,
    'domain_get_os_type': DomainGetOsType,
    'domain_get_vcpus': DomainGetVcpus,
    'connect_list_defined_domains': ConnectListDefinedDomains,
    'domain_lookup_by_id': DomainLookupById,
    'domain_lookup_by_name': DomainLookupByName,
    'domain_lookup_by_uuid': DomainLookupByUuid,
    'connect_num_of_defined_domains': ConnectNumOfDefinedDomains,
    'domain_pin_vcpu': DomainPinVcpu,
    'domain_reboot': DomainReboot,
    'domain_resume': DomainResume,
    'domain_set_autostart': DomainSetAutostart,
    'domain_set_max_memory': DomainSetMaxMemory,
    'domain_set_memory': DomainSetMemory,
    'domain_set_vcpus': DomainSetVcpus,
    'domain_shutdown': DomainShutdown,
    'domain_suspend': DomainSuspend,
    'domain_undefine': DomainUndefine,
    'connect_list_defined_networks': ConnectListDefinedNetworks,
    'connect_list_domains': ConnectListDomains,
    'connect_list_networks': ConnectListNetworks,
    'network_create': NetworkCreate,
    'network_create_xml': NetworkCreateXml,
    'network_define_xml': NetworkDefineXml,
    'network_destroy': NetworkDestroy,
    'network_get_xml_desc': NetworkGetXmlDesc,
    'network_get_autostart': NetworkGetAutostart,
    'network_get_bridge_name': NetworkGetBridgeName,
    'network_lookup_by_name': NetworkLookupByName,
    'network_lookup_by_uuid': NetworkLookupByUuid,
    'network_set_autostart': NetworkSetAutostart,
    'network_undefine': NetworkUndefine,
    'connect_num_of_defined_networks': ConnectNumOfDefinedNetworks,
    'connect_num_of_domains': ConnectNumOfDomains,
    'connect_num_of_networks': ConnectNumOfNetworks,
    'domain_core_dump': DomainCoreDump,
    'domain_restore': DomainRestore,
    'domain_save': DomainSave,
    'domain_get_scheduler_type': DomainGetSchedulerType,
    'domain_get_scheduler_parameters': DomainGetSchedulerParameters,
    'domain_set_scheduler_parameters': DomainSetSchedulerParameters,
    'connect_get_hostname': ConnectGetHostname,
    'connect_supports_feature': ConnectSupportsFeature,
    'domain_migrate_prepare': DomainMigratePrepare,
    'domain_migrate_perform': DomainMigratePerform,
    'domain_migrate_finish': DomainMigrateFinish,
    'domain_block_stats': DomainBlockStats,
    'domain_interface_stats': DomainInterfaceStats,
    'auth_list': AuthList,
    'auth_sasl_init': AuthSaslInit,
    'auth_sasl_start': AuthSaslStart,
    'auth_sasl_step': AuthSaslStep,
    'auth_polkit': AuthPolkit,
    'connect_num_of_storage_pools': ConnectNumOfStoragePools,
    'connect_list_storage_pools': ConnectListStoragePools,
    'connect_num_of_defined_storage_pools': ConnectNumOfDefinedStoragePools,
    'connect_list_defined_storage_pools': ConnectListDefinedStoragePools,
    'connect_find_storage_pool_sources': ConnectFindStoragePoolSources,
    'storage_pool_create_xml': StoragePoolCreateXml,
    'storage_pool_define_xml': StoragePoolDefineXml,
    'storage_pool_create': StoragePoolCreate,
    'storage_pool_build': StoragePoolBuild,
    'storage_pool_destroy': StoragePoolDestroy,
    'storage_pool_delete': StoragePoolDelete,
    'storage_pool_undefine': StoragePoolUndefine,
    'storage_pool_refresh': StoragePoolRefresh,
    'storage_pool_lookup_by_name': StoragePoolLookupByName,
    'storage_pool_lookup_by_uuid': StoragePoolLookupByUuid,
    'storage_pool_lookup_by_volume': StoragePoolLookupByVolume,
    'storage_pool_get_info': StoragePoolGetInfo,
    'storage_pool_get_xml_desc': StoragePoolGetXmlDesc,
    'storage_pool_get_autostart': StoragePoolGetAutostart,
    'storage_pool_set_autostart': StoragePoolSetAutostart,
    'storage_pool_num_of_volumes': StoragePoolNumOfVolumes,
    'storage_pool_list_volumes': StoragePoolListVolumes,
    'storage_vol_create_xml': StorageVolCreateXml,
    'storage_vol_delete': StorageVolDelete,
    'storage_vol_lookup_by_name': StorageVolLookupByName,
    'storage_vol_lookup_by_key': StorageVolLookupByKey,
    'storage_vol_lookup_by_path': StorageVolLookupByPath,
    'storage_vol_get_info': StorageVolGetInfo,
    'storage_vol_get_xml_desc': StorageVolGetXmlDesc,
    'storage_vol_get_path': StorageVolGetPath,
    'node_get_cells_free_memory': NodeGetCellsFreeMemory,
    'node_get_free_memory': NodeGetFreeMemory,
    'domain_block_peek': DomainBlockPeek,
    'domain_memory_peek': DomainMemoryPeek,
    'connect_domain_event_register': ConnectDomainEventRegister,
    'connect_domain_event_deregister': ConnectDomainEventDeregister,
    'domain_event_lifecycle': DomainEventLifecycle,
    'domain_migrate_prepare2': DomainMigratePrepare2,
    'domain_migrate_finish2': DomainMigrateFinish2,
    'connect_get_uri': ConnectGetUri,
    'node_num_of_devices': NodeNumOfDevices,
    'node_list_devices': NodeListDevices,
    'node_device_lookup_by_name': NodeDeviceLookupByName,
    'node_device_get_xml_desc': NodeDeviceGetXmlDesc,
    'node_device_get_parent': NodeDeviceGetParent,
    'node_device_num_of_caps': NodeDeviceNumOfCaps,
    'node_device_list_caps': NodeDeviceListCaps,
    'node_device_dettach': NodeDeviceDettach,
    'node_device_re_attach': NodeDeviceReAttach,
    'node_device_reset': NodeDeviceReset,
    'domain_get_security_label': DomainGetSecurityLabel,
    'node_get_security_model': NodeGetSecurityModel,
    'node_device_create_xml': NodeDeviceCreateXml,
    'node_device_destroy': NodeDeviceDestroy,
    'storage_vol_create_xml_from': StorageVolCreateXmlFrom,
    'connect_num_of_interfaces': ConnectNumOfInterfaces,
    'connect_list_interfaces': ConnectListInterfaces,
    'interface_lookup_by_name': InterfaceLookupByName,
    'interface_lookup_by_mac_string': InterfaceLookupByMacString,
    'interface_get_xml_desc': InterfaceGetXmlDesc,
    'interface_define_xml': InterfaceDefineXml,
    'interface_undefine': InterfaceUndefine,
    'interface_create': InterfaceCreate,
    'interface_destroy': InterfaceDestroy,
    'connect_domain_xml_from_native': ConnectDomainXmlFromNative,
    'connect_domain_xml_to_native': ConnectDomainXmlToNative,
    'connect_num_of_defined_interfaces': ConnectNumOfDefinedInterfaces,
    'connect_list_defined_interfaces': ConnectListDefinedInterfaces,
    'connect_num_of_secrets': ConnectNumOfSecrets,
    'connect_list_secrets': ConnectListSecrets,
    'secret_lookup_by_uuid': SecretLookupByUuid,
    'secret_define_xml': SecretDefineXml,
    'secret_get_xml_desc': SecretGetXmlDesc,
    'secret_set_value': SecretSetValue,
    'secret_get_value': SecretGetValue,
    'secret_undefine': SecretUndefine,
    'secret_lookup_by_usage': SecretLookupByUsage,
    'domain_migrate_prepare_tunnel': DomainMigratePrepareTunnel,
    'connect_is_secure': ConnectIsSecure,
    'domain_is_active': DomainIsActive,
    'domain_is_persistent': DomainIsPersistent,
    'network_is_active': NetworkIsActive,
    'network_is_persistent': NetworkIsPersistent,
    'storage_pool_is_active': StoragePoolIsActive,
    'storage_pool_is_persistent': StoragePoolIsPersistent,
    'interface_is_active': InterfaceIsActive,
    'connect_get_lib_version': ConnectGetLibVersion,
    'connect_compare_cpu': ConnectCompareCpu,
    'domain_memory_stats': DomainMemoryStats,
    'domain_attach_device_flags': DomainAttachDeviceFlags,
    'domain_detach_device_flags': DomainDetachDeviceFlags,
    'connect_baseline_cpu': ConnectBaselineCpu,
    'domain_get_job_info': DomainGetJobInfo,
    'domain_abort_job': DomainAbortJob,
    'storage_vol_wipe': StorageVolWipe,
    'domain_migrate_set_max_downtime': DomainMigrateSetMaxDowntime,
    'connect_domain_event_register_any': ConnectDomainEventRegisterAny,
    'connect_domain_event_deregister_any': ConnectDomainEventDeregisterAny,
    'domain_event_reboot': DomainEventReboot,
    'domain_event_rtc_change': DomainEventRtcChange,
    'domain_event_watchdog': DomainEventWatchdog,
    'domain_event_io_error': DomainEventIoError,
    'domain_event_graphics': DomainEventGraphics,
    'domain_update_device_flags': DomainUpdateDeviceFlags,
    'nwfilter_lookup_by_name': NwfilterLookupByName,
    'nwfilter_lookup_by_uuid': NwfilterLookupByUuid,
    'nwfilter_get_xml_desc': NwfilterGetXmlDesc,
    'connect_num_of_nwfilters': ConnectNumOfNwfilters,
    'connect_list_nwfilters': ConnectListNwfilters,
    'nwfilter_define_xml': NwfilterDefineXml,
    'nwfilter_undefine': NwfilterUndefine,
    'domain_managed_save': DomainManagedSave,
    'domain_has_managed_save_image': DomainHasManagedSaveImage,
    'domain_managed_save_remove': DomainManagedSaveRemove,
    'domain_snapshot_create_xml': DomainSnapshotCreateXml,
    'domain_snapshot_get_xml_desc': DomainSnapshotGetXmlDesc,
    'domain_snapshot_num': DomainSnapshotNum,
    'domain_snapshot_list_names': DomainSnapshotListNames,
    'domain_snapshot_lookup_by_name': DomainSnapshotLookupByName,
    'domain_has_current_snapshot': DomainHasCurrentSnapshot,
    'domain_snapshot_current': DomainSnapshotCurrent,
    'domain_revert_to_snapshot': DomainRevertToSnapshot,
    'domain_snapshot_delete': DomainSnapshotDelete,
    'domain_get_block_info': DomainGetBlockInfo,
    'domain_event_io_error_reason': DomainEventIoErrorReason,
    'domain_create_with_flags': DomainCreateWithFlags,
    'domain_set_memory_parameters': DomainSetMemoryParameters,
    'domain_get_memory_parameters': DomainGetMemoryParameters,
    'domain_set_vcpus_flags': DomainSetVcpusFlags,
    'domain_get_vcpus_flags': DomainGetVcpusFlags,
    'domain_open_console': DomainOpenConsole,
    'domain_is_updated': DomainIsUpdated,
    'connect_get_sysinfo': ConnectGetSysinfo,
    'domain_set_memory_flags': DomainSetMemoryFlags,
    'domain_set_blkio_parameters': DomainSetBlkioParameters,
    'domain_get_blkio_parameters': DomainGetBlkioParameters,
    'domain_migrate_set_max_speed': DomainMigrateSetMaxSpeed,
    'storage_vol_upload': StorageVolUpload,
    'storage_vol_download': StorageVolDownload,
    'domain_inject_nmi': DomainInjectNmi,
    'domain_screenshot': DomainScreenshot,
    'domain_get_state': DomainGetState,
    'domain_migrate_begin3': DomainMigrateBegin3,
    'domain_migrate_prepare3': DomainMigratePrepare3,
    'domain_migrate_prepare_tunnel3': DomainMigratePrepareTunnel3,
    'domain_migrate_perform3': DomainMigratePerform3,
    'domain_migrate_finish3': DomainMigrateFinish3,
    'domain_migrate_confirm3': DomainMigrateConfirm3,
    'domain_set_scheduler_parameters_flags': DomainSetSchedulerParametersFlags,
    'interface_change_begin': InterfaceChangeBegin,
    'interface_change_commit': InterfaceChangeCommit,
    'interface_change_rollback': InterfaceChangeRollback,
    'domain_get_scheduler_parameters_flags': DomainGetSchedulerParametersFlags,
    'domain_event_control_error': DomainEventControlError,
    'domain_pin_vcpu_flags': DomainPinVcpuFlags,
    'domain_send_key': DomainSendKey,
    'node_get_cpu_stats': NodeGetCpuStats,
    'node_get_memory_stats': NodeGetMemoryStats,
    'domain_get_control_info': DomainGetControlInfo,
    'domain_get_vcpu_pin_info': DomainGetVcpuPinInfo,
    'domain_undefine_flags': DomainUndefineFlags,
    'domain_save_flags': DomainSaveFlags,
    'domain_restore_flags': DomainRestoreFlags,
    'domain_destroy_flags': DomainDestroyFlags,
    'domain_save_image_get_xml_desc': DomainSaveImageGetXmlDesc,
    'domain_save_image_define_xml': DomainSaveImageDefineXml,
    'domain_block_job_abort': DomainBlockJobAbort,
    'domain_get_block_job_info': DomainGetBlockJobInfo,
    'domain_block_job_set_speed': DomainBlockJobSetSpeed,
    'domain_block_pull': DomainBlockPull,
    'domain_event_block_job': DomainEventBlockJob,
    'domain_migrate_get_max_speed': DomainMigrateGetMaxSpeed,
    'domain_block_stats_flags': DomainBlockStatsFlags,
    'domain_snapshot_get_parent': DomainSnapshotGetParent,
    'domain_reset': DomainReset,
    'domain_snapshot_num_children': DomainSnapshotNumChildren,
    'domain_snapshot_list_children_names': DomainSnapshotListChildrenNames,
    'domain_event_disk_change': DomainEventDiskChange,
    'domain_open_graphics': DomainOpenGraphics,
    'node_suspend_for_duration': NodeSuspendForDuration,
    'domain_block_resize': DomainBlockResize,
    'domain_set_block_io_tune': DomainSetBlockIoTune,
    'domain_get_block_io_tune': DomainGetBlockIoTune,
    'domain_set_numa_parameters': DomainSetNumaParameters,
    'domain_get_numa_parameters': DomainGetNumaParameters,
    'domain_set_interface_parameters': DomainSetInterfaceParameters,
    'domain_get_interface_parameters': DomainGetInterfaceParameters,
    'domain_shutdown_flags': DomainShutdownFlags,
    'storage_vol_wipe_pattern': StorageVolWipePattern,
    'storage_vol_resize': StorageVolResize,
    'domain_pm_suspend_for_duration': DomainPmSuspendForDuration,
    'domain_get_cpu_stats': DomainGetCpuStats,
    'domain_get_disk_errors': DomainGetDiskErrors,
    'domain_set_metadata': DomainSetMetadata,
    'domain_get_metadata': DomainGetMetadata,
    'domain_block_rebase': DomainBlockRebase,
    'domain_pm_wakeup': DomainPmWakeup,
    'domain_event_tray_change': DomainEventTrayChange,
    'domain_event_pmwakeup': DomainEventPmwakeup,
    'domain_event_pmsuspend': DomainEventPmsuspend,
    'domain_snapshot_is_current': DomainSnapshotIsCurrent,
    'domain_snapshot_has_metadata': DomainSnapshotHasMetadata,
    'connect_list_all_domains': ConnectListAllDomains,
    'domain_list_all_snapshots': DomainListAllSnapshots,
    'domain_snapshot_list_all_children': DomainSnapshotListAllChildren,
    'domain_event_balloon_change': DomainEventBalloonChange,
    'domain_get_hostname': DomainGetHostname,
    'domain_get_security_label_list': DomainGetSecurityLabelList,
    'domain_pin_emulator': DomainPinEmulator,
    'domain_get_emulator_pin_info': DomainGetEmulatorPinInfo,
    'connect_list_all_storage_pools': ConnectListAllStoragePools,
    'storage_pool_list_all_volumes': StoragePoolListAllVolumes,
    'connect_list_all_networks': ConnectListAllNetworks,
    'connect_list_all_interfaces': ConnectListAllInterfaces,
    'connect_list_all_node_devices': ConnectListAllNodeDevices,
    'connect_list_all_nwfilters': ConnectListAllNwfilters,
    'connect_list_all_secrets': ConnectListAllSecrets,
    'node_set_memory_parameters': NodeSetMemoryParameters,
    'node_get_memory_parameters': NodeGetMemoryParameters,
    'domain_block_commit': DomainBlockCommit,
    'network_update': NetworkUpdate,
    'domain_event_pmsuspend_disk': DomainEventPmsuspendDisk,
    'node_get_cpu_map': NodeGetCpuMap,
    'domain_fstrim': DomainFstrim,
    'domain_send_process_signal': DomainSendProcessSignal,
    'domain_open_channel': DomainOpenChannel,
    'node_device_lookup_scsi_host_by_wwn': NodeDeviceLookupScsiHostByWwn,
    'domain_get_job_stats': DomainGetJobStats,
    'domain_migrate_get_compression_cache': DomainMigrateGetCompressionCache,
    'domain_migrate_set_compression_cache': DomainMigrateSetCompressionCache,
    'node_device_detach_flags': NodeDeviceDetachFlags,
    'domain_migrate_begin3_params': DomainMigrateBegin3Params,
    'domain_migrate_prepare3_params': DomainMigratePrepare3Params,
    'domain_migrate_prepare_tunnel3_params': DomainMigratePrepareTunnel3Params,
    'domain_migrate_perform3_params': DomainMigratePerform3Params,
    'domain_migrate_finish3_params': DomainMigrateFinish3Params,
    'domain_migrate_confirm3_params': DomainMigrateConfirm3Params,
    'domain_set_memory_stats_period': DomainSetMemoryStatsPeriod,
    'domain_create_xml_with_files': DomainCreateXmlWithFiles,
    'domain_create_with_files': DomainCreateWithFiles,
    'domain_event_device_removed': DomainEventDeviceRemoved,
    'connect_get_cpu_model_names': ConnectGetCpuModelNames,
}
PROCEDURE_BY_ID = {
    1: ConnectOpen,
    2: ConnectClose,
    3: ConnectGetType,
    4: ConnectGetVersion,
    5: ConnectGetMaxVcpus,
    6: NodeGetInfo,
    7: ConnectGetCapabilities,
    8: DomainAttachDevice,
    9: DomainCreate,
    10: DomainCreateXml,
    11: DomainDefineXml,
    12: DomainDestroy,
    13: DomainDetachDevice,
    14: DomainGetXmlDesc,
    15: DomainGetAutostart,
    16: DomainGetInfo,
    17: DomainGetMaxMemory,
    18: DomainGetMaxVcpus,
    19: DomainGetOsType,
    20: DomainGetVcpus,
    21: ConnectListDefinedDomains,
    22: DomainLookupById,
    23: DomainLookupByName,
    24: DomainLookupByUuid,
    25: ConnectNumOfDefinedDomains,
    26: DomainPinVcpu,
    27: DomainReboot,
    28: DomainResume,
    29: DomainSetAutostart,
    30: DomainSetMaxMemory,
    31: DomainSetMemory,
    32: DomainSetVcpus,
    33: DomainShutdown,
    34: DomainSuspend,
    35: DomainUndefine,
    36: ConnectListDefinedNetworks,
    37: ConnectListDomains,
    38: ConnectListNetworks,
    39: NetworkCreate,
    40: NetworkCreateXml,
    41: NetworkDefineXml,
    42: NetworkDestroy,
    43: NetworkGetXmlDesc,
    44: NetworkGetAutostart,
    45: NetworkGetBridgeName,
    46: NetworkLookupByName,
    47: NetworkLookupByUuid,
    48: NetworkSetAutostart,
    49: NetworkUndefine,
    50: ConnectNumOfDefinedNetworks,
    51: ConnectNumOfDomains,
    52: ConnectNumOfNetworks,
    53: DomainCoreDump,
    54: DomainRestore,
    55: DomainSave,
    56: DomainGetSchedulerType,
    57: DomainGetSchedulerParameters,
    58: DomainSetSchedulerParameters,
    59: ConnectGetHostname,
    60: ConnectSupportsFeature,
    61: DomainMigratePrepare,
    62: DomainMigratePerform,
    63: DomainMigrateFinish,
    64: DomainBlockStats,
    65: DomainInterfaceStats,
    66: AuthList,
    67: AuthSaslInit,
    68: AuthSaslStart,
    69: AuthSaslStep,
    70: AuthPolkit,
    71: ConnectNumOfStoragePools,
    72: ConnectListStoragePools,
    73: ConnectNumOfDefinedStoragePools,
    74: ConnectListDefinedStoragePools,
    75: ConnectFindStoragePoolSources,
    76: StoragePoolCreateXml,
    77: StoragePoolDefineXml,
    78: StoragePoolCreate,
    79: StoragePoolBuild,
    80: StoragePoolDestroy,
    81: StoragePoolDelete,
    82: StoragePoolUndefine,
    83: StoragePoolRefresh,
    84: StoragePoolLookupByName,
    85: StoragePoolLookupByUuid,
    86: StoragePoolLookupByVolume,
    87: StoragePoolGetInfo,
    88: StoragePoolGetXmlDesc,
    89: StoragePoolGetAutostart,
    90: StoragePoolSetAutostart,
    91: StoragePoolNumOfVolumes,
    92: StoragePoolListVolumes,
    93: StorageVolCreateXml,
    94: StorageVolDelete,
    95: StorageVolLookupByName,
    96: StorageVolLookupByKey,
    97: StorageVolLookupByPath,
    98: StorageVolGetInfo,
    99: StorageVolGetXmlDesc,
    100: StorageVolGetPath,
    101: NodeGetCellsFreeMemory,
    102: NodeGetFreeMemory,
    103: DomainBlockPeek,
    104: DomainMemoryPeek,
    105: ConnectDomainEventRegister,
    106: ConnectDomainEventDeregister,
    107: DomainEventLifecycle,
    108: DomainMigratePrepare2,
    109: DomainMigrateFinish2,
    110: ConnectGetUri,
    111: NodeNumOfDevices,
    112: NodeListDevices,
    113: NodeDeviceLookupByName,
    114: NodeDeviceGetXmlDesc,
    115: NodeDeviceGetParent,
    116: NodeDeviceNumOfCaps,
    117: NodeDeviceListCaps,
    118: NodeDeviceDettach,
    119: NodeDeviceReAttach,
    120: NodeDeviceReset,
    121: DomainGetSecurityLabel,
    122: NodeGetSecurityModel,
    123: NodeDeviceCreateXml,
    124: NodeDeviceDestroy,
    125: StorageVolCreateXmlFrom,
    126: ConnectNumOfInterfaces,
    127: ConnectListInterfaces,
    128: InterfaceLookupByName,
    129: InterfaceLookupByMacString,
    130: InterfaceGetXmlDesc,
    131: InterfaceDefineXml,
    132: InterfaceUndefine,
    133: InterfaceCreate,
    134: InterfaceDestroy,
    135: ConnectDomainXmlFromNative,
    136: ConnectDomainXmlToNative,
    137: ConnectNumOfDefinedInterfaces,
    138: ConnectListDefinedInterfaces,
    139: ConnectNumOfSecrets,
    140: ConnectListSecrets,
    141: SecretLookupByUuid,
    142: SecretDefineXml,
    143: SecretGetXmlDesc,
    144: SecretSetValue,
    145: SecretGetValue,
    146: SecretUndefine,
    147: SecretLookupByUsage,
    148: DomainMigratePrepareTunnel,
    149: ConnectIsSecure,
    150: DomainIsActive,
    151: DomainIsPersistent,
    152: NetworkIsActive,
    153: NetworkIsPersistent,
    154: StoragePoolIsActive,
    155: StoragePoolIsPersistent,
    156: InterfaceIsActive,
    157: ConnectGetLibVersion,
    158: ConnectCompareCpu,
    159: DomainMemoryStats,
    160: DomainAttachDeviceFlags,
    161: DomainDetachDeviceFlags,
    162: ConnectBaselineCpu,
    163: DomainGetJobInfo,
    164: DomainAbortJob,
    165: StorageVolWipe,
    166: DomainMigrateSetMaxDowntime,
    167: ConnectDomainEventRegisterAny,
    168: ConnectDomainEventDeregisterAny,
    169: DomainEventReboot,
    170: DomainEventRtcChange,
    171: DomainEventWatchdog,
    172: DomainEventIoError,
    173: DomainEventGraphics,
    174: DomainUpdateDeviceFlags,
    175: NwfilterLookupByName,
    176: NwfilterLookupByUuid,
    177: NwfilterGetXmlDesc,
    178: ConnectNumOfNwfilters,
    179: ConnectListNwfilters,
    180: NwfilterDefineXml,
    181: NwfilterUndefine,
    182: DomainManagedSave,
    183: DomainHasManagedSaveImage,
    184: DomainManagedSaveRemove,
    185: DomainSnapshotCreateXml,
    186: DomainSnapshotGetXmlDesc,
    187: DomainSnapshotNum,
    188: DomainSnapshotListNames,
    189: DomainSnapshotLookupByName,
    190: DomainHasCurrentSnapshot,
    191: DomainSnapshotCurrent,
    192: DomainRevertToSnapshot,
    193: DomainSnapshotDelete,
    194: DomainGetBlockInfo,
    195: DomainEventIoErrorReason,
    196: DomainCreateWithFlags,
    197: DomainSetMemoryParameters,
    198: DomainGetMemoryParameters,
    199: DomainSetVcpusFlags,
    200: DomainGetVcpusFlags,
    201: DomainOpenConsole,
    202: DomainIsUpdated,
    203: ConnectGetSysinfo,
    204: DomainSetMemoryFlags,
    205: DomainSetBlkioParameters,
    206: DomainGetBlkioParameters,
    207: DomainMigrateSetMaxSpeed,
    208: StorageVolUpload,
    209: StorageVolDownload,
    210: DomainInjectNmi,
    211: DomainScreenshot,
    212: DomainGetState,
    213: DomainMigrateBegin3,
    214: DomainMigratePrepare3,
    215: DomainMigratePrepareTunnel3,
    216: DomainMigratePerform3,
    217: DomainMigrateFinish3,
    218: DomainMigrateConfirm3,
    219: DomainSetSchedulerParametersFlags,
    220: InterfaceChangeBegin,
    221: InterfaceChangeCommit,
    222: InterfaceChangeRollback,
    223: DomainGetSchedulerParametersFlags,
    224: DomainEventControlError,
    225: DomainPinVcpuFlags,
    226: DomainSendKey,
    227: NodeGetCpuStats,
    228: NodeGetMemoryStats,
    229: DomainGetControlInfo,
    230: DomainGetVcpuPinInfo,
    231: DomainUndefineFlags,
    232: DomainSaveFlags,
    233: DomainRestoreFlags,
    234: DomainDestroyFlags,
    235: DomainSaveImageGetXmlDesc,
    236: DomainSaveImageDefineXml,
    237: DomainBlockJobAbort,
    238: DomainGetBlockJobInfo,
    239: DomainBlockJobSetSpeed,
    240: DomainBlockPull,
    241: DomainEventBlockJob,
    242: DomainMigrateGetMaxSpeed,
    243: DomainBlockStatsFlags,
    244: DomainSnapshotGetParent,
    245: DomainReset,
    246: DomainSnapshotNumChildren,
    247: DomainSnapshotListChildrenNames,
    248: DomainEventDiskChange,
    249: DomainOpenGraphics,
    250: NodeSuspendForDuration,
    251: DomainBlockResize,
    252: DomainSetBlockIoTune,
    253: DomainGetBlockIoTune,
    254: DomainSetNumaParameters,
    255: DomainGetNumaParameters,
    256: DomainSetInterfaceParameters,
    257: DomainGetInterfaceParameters,
    258: DomainShutdownFlags,
    259: StorageVolWipePattern,
    260: StorageVolResize,
    261: DomainPmSuspendForDuration,
    262: DomainGetCpuStats,
    263: DomainGetDiskErrors,
    264: DomainSetMetadata,
    265: DomainGetMetadata,
    266: DomainBlockRebase,
    267: DomainPmWakeup,
    268: DomainEventTrayChange,
    269: DomainEventPmwakeup,
    270: DomainEventPmsuspend,
    271: DomainSnapshotIsCurrent,
    272: DomainSnapshotHasMetadata,
    273: ConnectListAllDomains,
    274: DomainListAllSnapshots,
    275: DomainSnapshotListAllChildren,
    276: DomainEventBalloonChange,
    277: DomainGetHostname,
    278: DomainGetSecurityLabelList,
    279: DomainPinEmulator,
    280: DomainGetEmulatorPinInfo,
    281: ConnectListAllStoragePools,
    282: StoragePoolListAllVolumes,
    283: ConnectListAllNetworks,
    284: ConnectListAllInterfaces,
    285: ConnectListAllNodeDevices,
    286: ConnectListAllNwfilters,
    287: ConnectListAllSecrets,
    288: NodeSetMemoryParameters,
    289: NodeGetMemoryParameters,
    290: DomainBlockCommit,
    291: NetworkUpdate,
    292: DomainEventPmsuspendDisk,
    293: NodeGetCpuMap,
    294: DomainFstrim,
    295: DomainSendProcessSignal,
    296: DomainOpenChannel,
    297: NodeDeviceLookupScsiHostByWwn,
    298: DomainGetJobStats,
    299: DomainMigrateGetCompressionCache,
    300: DomainMigrateSetCompressionCache,
    301: NodeDeviceDetachFlags,
    302: DomainMigrateBegin3Params,
    303: DomainMigratePrepare3Params,
    304: DomainMigratePrepareTunnel3Params,
    305: DomainMigratePerform3Params,
    306: DomainMigrateFinish3Params,
    307: DomainMigrateConfirm3Params,
    308: DomainSetMemoryStatsPeriod,
    309: DomainCreateXmlWithFiles,
    310: DomainCreateWithFiles,
    311: DomainEventDeviceRemoved,
    312: ConnectGetCpuModelNames,
}
