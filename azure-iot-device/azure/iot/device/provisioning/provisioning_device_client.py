# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
This module contains user-facing synchronous Provisioning Device Client for Azure Provisioning
Device SDK. This client uses Symmetric Key and X509 authentication to register devices with an
IoT Hub via the Device Provisioning Service.
"""
import logging
from azure.iot.device.common.evented_callback import EventedCallback
from .abstract_provisioning_device_client import AbstractProvisioningDeviceClient
from .abstract_provisioning_device_client import log_on_register_complete
from .internal.polling_machine import PollingMachine

logger = logging.getLogger(__name__)


class ProvisioningDeviceClient(AbstractProvisioningDeviceClient):
    """
    Client which can be used to run the registration of a device with provisioning service
    using Symmetric Key authentication.
    """

    def __init__(self, provisioning_pipeline):
        """
        Initializer for the Provisioning Client.

        NOTE: This initializer should not be called directly.
        Instead, the class methods that start with `create_from_` should be used to create a
        client object.

        :param provisioning_pipeline: The protocol pipeline for provisioning.
        :type provisioning_pipeline: :class:`azure.iot.device.provisioning.pipeline.ProvisioningPipeline`
        """
        super(ProvisioningDeviceClient, self).__init__(provisioning_pipeline)
        self._polling_machine = PollingMachine(provisioning_pipeline)

    def register(self):
        """
        Register the device with the with the provisioning service

        This is a synchronous call, meaning that this function will not return until the
        registration process has completed successfully or the attempt has resulted in a failure.
        Before returning, the client will also disconnect from the provisioning service.
        If a registration attempt is made while a previous registration is in progress it may
        throw an error.

        :returns: RegistrationResult indicating the result of the registration.
        :rtype: :class:`azure.iot.device.RegistrationResult`
        """
        logger.info("Registering with Provisioning Service...")

        register_complete = EventedCallback(return_arg_name="result")
        self._polling_machine.register(
            payload=self._provisioning_payload, callback=register_complete
        )
        result = register_complete.wait_for_completion()

        log_on_register_complete(result)
        return result
