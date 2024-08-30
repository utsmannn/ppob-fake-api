from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MerchantAccount:
    identifier: str = ""  # 26/51 / 00
    merchant_id: str = ""  # 26/51 / 02
    merchant_pan: str = ""  # 26/51 / 01
    merchant_criteria: str = ""  # 26/51 / 03


@dataclass
class AdditionalInfo:
    reference_label: str = ""  # 62 / 05
    terminal_label: str = ""  # 62 / 07
    payment_system_specified_template: str = ""  # 62 / 50


@dataclass
class QrisData:
    raw: str = ""
    format_indicator: str = ""  # 00
    initiation_method: str = ""  # 01
    amount: str = ""  # 54
    merchant_name: str = ""  # 59
    merchant_city: str = ""  # 60
    country_code: str = ""  # 58
    postal_code: str = ""  # 61
    merchant_account_1: MerchantAccount = field(default_factory=MerchantAccount)  # 26
    merchant_account_2: MerchantAccount = field(default_factory=MerchantAccount)  # 51
    additional_info: AdditionalInfo = field(default_factory=AdditionalInfo)  # 62
    crc: str = ""  # 63


def qris_processor(result: dict) -> QrisData:
    qris_data = QrisData()

    mapping = {
        "00": "format_indicator",
        "01": "initiation_method",
        "54": "amount",
        "59": "merchant_name",
        "60": "merchant_city",
        "58": "country_code",
        "61": "postal_code",
        "26-00": "merchant_account_1.identifier",
        "26-01": "merchant_account_1.merchant_pan",
        "26-02": "merchant_account_1.merchant_id",
        "26-03": "merchant_account_1.merchant_criteria",
        "51-00": "merchant_account_2.identifier",
        "51-01": "merchant_account_2.merchant_pan",
        "51-02": "merchant_account_2.merchant_id",
        "51-03": "merchant_account_2.merchant_criteria",
        "62-05": "additional_info.reference_label",
        "62-07": "additional_info.terminal_label",
        "62-50": "additional_info.payment_system_specified_template",
        "63": "crc"
    }

    for t, u in result.items():
        if t in mapping:
            attr_path = mapping[t].split(".")
            target = qris_data
            for attr in attr_path[:-1]:
                target = getattr(target, attr)
            setattr(target, attr_path[-1], u)

    return qris_data


def parse_qris(input_string: str) -> Optional[QrisData]:
    index = 0
    result = {}

    while index < len(input_string):
        qr_id = input_string[index:index + 2]
        qr_id_length = input_string[index + 2:index + 4]

        try:
            qr_id_value_length = int(qr_id_length)
        except ValueError:
            return None

        qr_id_value = input_string[index + 4:index + 4 + qr_id_value_length]
        result[qr_id] = qr_id_value

        if 26 <= int(qr_id) <= 40 or int(qr_id) in [51, 62]:
            nested_index = 0
            while nested_index < len(qr_id_value):
                try:
                    nqi = qr_id_value[nested_index:nested_index + 2]  # nested qr id
                    nqi_length = qr_id_value[nested_index + 2:nested_index + 4]
                    nqi_value_length = int(nqi_length)
                    nqi_value_index = int(nested_index + 4)
                    nqi_value_index_offset = int(nested_index + 4 + nqi_value_length)
                    nqi_value = qr_id_value[nqi_value_index:nqi_value_index_offset]

                    result[f"{qr_id}-{nqi}"] = nqi_value
                    nested_index += 4 + nqi_value_length
                except ValueError:
                    # except when index invalid
                    return None

        index += 4 + qr_id_value_length

    qris_data = qris_processor(result)
    qris_data.raw = input_string
    if qris_data.merchant_account_2.identifier == 'ID.CO.QRIS.WWW':
        return qris_data
    else:
        return None  # invalid QRIS provider
