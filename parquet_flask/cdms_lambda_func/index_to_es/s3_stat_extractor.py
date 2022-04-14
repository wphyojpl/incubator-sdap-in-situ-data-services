from parquet_flask.io_logic.cdms_constants import CDMSConstants


class S3StatExtractor:
    def __init__(self, s3_url: str):
        self.__s3_url = s3_url
        self.__provider = None
        self.__project = None
        self.__platform_code = None
        self.__geo_interval = None
        self.__year = None
        self.__month = None
        self.__job_id = None
        self.__name = None
        self.__bucket = None

    @property
    def bucket(self):
        return self.__bucket

    @bucket.setter
    def bucket(self, val):
        """
        :param val:
        :return: None
        """
        self.__bucket = val
        return

    @property
    def job_id(self):
        return self.__job_id

    @job_id.setter
    def job_id(self, val):
        """
        :param val:
        :return: None
        """
        self.__job_id = val
        return

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        """
        :param val:
        :return: None
        """
        self.__name = val
        return

    @property
    def provider(self):
        return self.__provider

    @provider.setter
    def provider(self, val):
        """
        :param val:
        :return: None
        """
        self.__provider = val
        return

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, val):
        """
        :param val:
        :return: None
        """
        self.__project = val
        return

    @property
    def platform_code(self):
        return self.__platform_code

    @platform_code.setter
    def platform_code(self, val):
        """
        :param val:
        :return: None
        """
        self.__platform_code = val
        return

    @property
    def geo_interval(self):
        return self.__geo_interval

    @geo_interval.setter
    def geo_interval(self, val):
        """
        :param val:
        :return: None
        """
        self.__geo_interval = val
        return

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, val):
        """
        :param val:
        :return: None
        """
        self.__year = val
        return

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, val):
        """
        :param val:
        :return: None
        """
        self.__month = val
        return

    def start(self):
        split_s3_url = self.__s3_url.split('://')
        if len(split_s3_url) != 2:
            raise ValueError(f'invalid S3 URL: {self.__s3_url}')
        split_s3_path = split_s3_url[1].strip().split('/')
        if len(split_s3_path) < 2:
            raise ValueError(f'invalid s3 path: {split_s3_url[1]}')
        self.bucket = split_s3_path[0]
        self.name = split_s3_path[-1]

        partition_dict = [k.split('=') for k in split_s3_path[1: -1]]
        partition_dict = {k[0]: k[1] for k in partition_dict}

        if CDMSConstants.provider_col in partition_dict:
            self.provider = partition_dict[CDMSConstants.provider_col]

        if CDMSConstants.project_col in partition_dict:
            self.project = partition_dict[CDMSConstants.project_col]

        if CDMSConstants. in partition_dict:
            self.platform_code = partition_dict[CDMSConstants.platform_code_col]

        if CDMSConstants. in partition_dict:
            self.platform_code = partition_dict[CDMSConstants.platform_code_col]

        if CDMSConstants.year_col in partition_dict:
            self.year = partition_dict[CDMSConstants.year_col]

        if CDMSConstants.month_col in partition_dict:
            self.month = partition_dict[CDMSConstants.month_col]

        if CDMSConstants.job_id_col in partition_dict:
            self.job_id = partition_dict[CDMSConstants.job_id_col]


        return self
